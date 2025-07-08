using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.Formats;
using SixLabors.ImageSharp.Formats.Bmp;
using SixLabors.ImageSharp.Formats.Gif;
using SixLabors.ImageSharp.Formats.Jpeg;
using SixLabors.ImageSharp.Formats.Png;
using SixLabors.ImageSharp.Formats.Tiff;
using SixLabors.ImageSharp.Processing;
using Image = SixLabors.ImageSharp.Image;

namespace XConvertor
{
    public partial class Form1 : Form
    {
        private readonly Dictionary<string, List<string>> _conversionMap;
        private string _droppedFilePath;
        private List<string> _imageExtensions = new List<string> { ".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff" };
        private List<string> _videoExtensions = new List<string> { ".mp4", ".avi", ".mkv", ".mov", ".wmv" };

        public Form1()
        {
            InitializeComponent();
            _conversionMap = new Dictionary<string, List<string>>(StringComparer.OrdinalIgnoreCase)
            {
                { ".jpg", _imageExtensions.Where(ext => ext != ".jpg" && ext != ".jpeg").ToList() },
                { ".jpeg", _imageExtensions.Where(ext => ext != ".jpg" && ext != ".jpeg").ToList() },
                { ".png", _imageExtensions.Where(ext => ext != ".png").ToList() },
                { ".bmp", _imageExtensions.Where(ext => ext != ".bmp").ToList() },
                { ".gif", _imageExtensions.Where(ext => ext != ".gif").ToList() },
                { ".tiff", _imageExtensions.Where(ext => ext != ".tiff").ToList() },

                // --- ЗАГЛУШКИ ДЛЯ БУДУЩИХ КОНВЕРТАЦИЙ ---
                // Видео
                { ".mp4", _videoExtensions.Where(ext => ext != ".mp4").ToList() },
                { ".avi", _videoExtensions.Where(ext => ext != ".avi").ToList() },
                { ".mkv", _videoExtensions.Where(ext => ext != ".mkv").ToList() },
                
                // Документы
                { ".docx", new List<string> { ".pdf", ".txt" } },
                { ".pdf", new List<string> { ".docx", ".txt", ".jpg", ".png" } },
            };
        }

        private void Form1_DragEnter(object sender, DragEventArgs e)
        {
            if (e.Data.GetDataPresent(DataFormats.FileDrop))
                e.Effect = DragDropEffects.Copy;
        }

        private void Form1_DragDrop(object sender, DragEventArgs e)
        {
            string[] files = (string[])e.Data.GetData(DataFormats.FileDrop);
            if (files.Length > 0)
            {
                ResetToInitialState();
                ProcessFile(files[0]);
            }
        }

        private void ResetToInitialState()
        {
            lblDragAndDrop.Visible = true;
            splitContainer.Visible = false;
            _droppedFilePath = null;
            lstConversionOptions.Items.Clear();
            picFileIcon.Image = null;
        }

        private void ProcessFile(string filePath)
        {
            _droppedFilePath = filePath;
            string extension = Path.GetExtension(filePath).ToLower();
            string fileName = Path.GetFileName(filePath);

            if (_conversionMap.ContainsKey(extension))
            {
                lblDragAndDrop.Visible = false;
                splitContainer.Visible = true;

                lblFileName.Text = fileName;
                if (_imageExtensions.Contains(extension))
                {
                    try { picFileIcon.Image = System.Drawing.Image.FromFile(filePath); }
                    catch {}
                }
                if (picFileIcon.Image == null)
                {
                    try { picFileIcon.Image = Icon.ExtractAssociatedIcon(filePath)?.ToBitmap(); }
                    catch { picFileIcon.Image = SystemIcons.WinLogo.ToBitmap(); }
                }

                lstConversionOptions.Items.Clear();
                _conversionMap[extension].ForEach(ext => lstConversionOptions.Items.Add(ext));
                if (lstConversionOptions.Items.Count > 0)
                    lstConversionOptions.SelectedIndex = 0;
            }
            else
            {
                ShowUnknownFileError(extension);
            }
        }

        private void ShowUnknownFileError(string extension)
        {
            string message = $"Файл с расширением \"{extension}\" не поддерживается.\n\nХотите найти информацию об этом формате в интернете?";
            var result = MessageBox.Show(message, "Неизвестный тип файла", MessageBoxButtons.YesNo, MessageBoxIcon.Error);
            if (result == DialogResult.Yes)
            {
                Process.Start($"https://www.google.com/search?q={extension}+file+converter");
            }
        }

        private async void BtnConvert_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrEmpty(_droppedFilePath) || lstConversionOptions.SelectedItem == null) return;

            string targetExtension = lstConversionOptions.SelectedItem.ToString();
            string sourceExtension = Path.GetExtension(_droppedFilePath).ToLower();

            using (SaveFileDialog saveDialog = new SaveFileDialog())
            {
                saveDialog.FileName = Path.GetFileNameWithoutExtension(_droppedFilePath) + targetExtension;
                saveDialog.Filter = $"Файл ({targetExtension})|*{targetExtension}";
                if (saveDialog.ShowDialog() != DialogResult.OK) return;

                string savePath = saveDialog.FileName;

                SetConversionState(true);

                try
                {
                    bool success = false;
                    if (_imageExtensions.Contains(sourceExtension))
                    {
                        await Task.Run(() => ConvertImage(_droppedFilePath, savePath, targetExtension));
                        success = true;
                    }
                    else if (_videoExtensions.Contains(sourceExtension))
                    {
                        MessageBox.Show("Конвертация видео еще не реализована.", "В разработке", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }
                    else
                    {
                        MessageBox.Show("Конвертация документов еще не реализована.", "В разработке", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }

                    if (success)
                        MessageBox.Show("Файл успешно конвертирован!", "Готово", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Произошла ошибка во время конвертации:\n{ex.Message}", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                finally
                {
                    SetConversionState(false);
                }
            }
        }

        private void SetConversionState(bool isConverting)
        {
            progressBar.Visible = isConverting;
            btnConvert.Enabled = !isConverting;
            lstConversionOptions.Enabled = !isConverting;
            this.AllowDrop = !isConverting;
        }

        private void ConvertImage(string sourcePath, string savePath, string targetExtension)
        {
            using (Image image = Image.Load(sourcePath))
            {
                IImageEncoder encoder = GetEncoder(targetExtension);
                image.Save(savePath, encoder);
            }
        }
        private IImageEncoder GetEncoder(string extension)
        {
            switch (extension.ToLower())
            {
                case ".png": return new PngEncoder();
                case ".jpg":
                case ".jpeg": return new JpegEncoder { Quality = 100 };
                case ".bmp": return new BmpEncoder();
                case ".gif": return new GifEncoder();
                case ".tiff": return new TiffEncoder();
                default: throw new NotSupportedException($"Формат {extension} не поддерживается для сохранения.");
            }
        }
    }
}