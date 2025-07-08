namespace XConvertor
{
    partial class Form1
    {
        private System.ComponentModel.IContainer components = null;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        private void InitializeComponent()
        {
            this.lblDragAndDrop = new System.Windows.Forms.Label();
            this.splitContainer = new System.Windows.Forms.SplitContainer();
            this.pnlFileInfo = new System.Windows.Forms.Panel();
            this.lblFileName = new System.Windows.Forms.Label();
            this.picFileIcon = new System.Windows.Forms.PictureBox();
            this.pnlConversionOptions = new System.Windows.Forms.Panel();
            this.progressBar = new System.Windows.Forms.ProgressBar();
            this.btnConvert = new System.Windows.Forms.Button();
            this.lblConvertTo = new System.Windows.Forms.Label();
            this.lstConversionOptions = new System.Windows.Forms.ListBox();
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer)).BeginInit();
            this.splitContainer.Panel1.SuspendLayout();
            this.splitContainer.Panel2.SuspendLayout();
            this.splitContainer.SuspendLayout();
            this.pnlFileInfo.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.picFileIcon)).BeginInit();
            this.pnlConversionOptions.SuspendLayout();
            this.SuspendLayout();
            // 
            // lblDragAndDrop
            // 
            this.lblDragAndDrop.Dock = System.Windows.Forms.DockStyle.Fill;
            this.lblDragAndDrop.Font = new System.Drawing.Font("Segoe UI", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(204)));
            this.lblDragAndDrop.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(224)))), ((int)(((byte)(224)))), ((int)(((byte)(224)))));
            this.lblDragAndDrop.Location = new System.Drawing.Point(0, 0);
            this.lblDragAndDrop.Name = "lblDragAndDrop";
            this.lblDragAndDrop.Size = new System.Drawing.Size(800, 450);
            this.lblDragAndDrop.TabIndex = 0;
            this.lblDragAndDrop.Text = "Перетащите файл";
            this.lblDragAndDrop.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // splitContainer
            // 
            this.splitContainer.Dock = System.Windows.Forms.DockStyle.Fill;
            this.splitContainer.IsSplitterFixed = true;
            this.splitContainer.Location = new System.Drawing.Point(0, 0);
            this.splitContainer.Name = "splitContainer";
            // 
            // splitContainer.Panel1
            // 
            this.splitContainer.Panel1.Controls.Add(this.pnlFileInfo);
            // 
            // splitContainer.Panel2
            // 
            this.splitContainer.Panel2.Controls.Add(this.pnlConversionOptions);
            this.splitContainer.Size = new System.Drawing.Size(800, 450);
            this.splitContainer.SplitterDistance = 400;
            this.splitContainer.TabIndex = 1;
            this.splitContainer.Visible = false;
            // 
            // pnlFileInfo
            // 
            this.pnlFileInfo.Controls.Add(this.lblFileName);
            this.pnlFileInfo.Controls.Add(this.picFileIcon);
            this.pnlFileInfo.Dock = System.Windows.Forms.DockStyle.Fill;
            this.pnlFileInfo.Location = new System.Drawing.Point(0, 0);
            this.pnlFileInfo.Name = "pnlFileInfo";
            this.pnlFileInfo.Size = new System.Drawing.Size(400, 450);
            this.pnlFileInfo.TabIndex = 0;
            // 
            // lblFileName
            // 
            this.lblFileName.Font = new System.Drawing.Font("Segoe UI", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(204)));
            this.lblFileName.ForeColor = System.Drawing.Color.White;
            this.lblFileName.Location = new System.Drawing.Point(12, 273);
            this.lblFileName.Name = "lblFileName";
            this.lblFileName.Size = new System.Drawing.Size(376, 54);
            this.lblFileName.TabIndex = 1;
            this.lblFileName.Text = "FileName.ext";
            this.lblFileName.TextAlign = System.Drawing.ContentAlignment.TopCenter;
            // 
            // picFileIcon
            // 
            this.picFileIcon.Location = new System.Drawing.Point(136, 143);
            this.picFileIcon.Name = "picFileIcon";
            this.picFileIcon.Size = new System.Drawing.Size(128, 128);
            this.picFileIcon.SizeMode = System.Windows.Forms.PictureBoxSizeMode.Zoom;
            this.picFileIcon.TabIndex = 0;
            this.picFileIcon.TabStop = false;
            // 
            // pnlConversionOptions
            // 
            this.pnlConversionOptions.Controls.Add(this.progressBar);
            this.pnlConversionOptions.Controls.Add(this.btnConvert);
            this.pnlConversionOptions.Controls.Add(this.lblConvertTo);
            this.pnlConversionOptions.Controls.Add(this.lstConversionOptions);
            this.pnlConversionOptions.Dock = System.Windows.Forms.DockStyle.Fill;
            this.pnlConversionOptions.Location = new System.Drawing.Point(0, 0);
            this.pnlConversionOptions.Name = "pnlConversionOptions";
            this.pnlConversionOptions.Size = new System.Drawing.Size(396, 450);
            this.pnlConversionOptions.TabIndex = 0;
            // 
            // progressBar
            // 
            this.progressBar.Location = new System.Drawing.Point(20, 381);
            this.progressBar.Name = "progressBar";
            this.progressBar.Size = new System.Drawing.Size(356, 10);
            this.progressBar.Style = System.Windows.Forms.ProgressBarStyle.Marquee;
            this.progressBar.TabIndex = 3;
            this.progressBar.Visible = false;
            // 
            // btnConvert
            // 
            this.btnConvert.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(123)))), ((int)(((byte)(255)))));
            this.btnConvert.FlatAppearance.BorderSize = 0;
            this.btnConvert.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.btnConvert.Font = new System.Drawing.Font("Segoe UI", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(204)));
            this.btnConvert.ForeColor = System.Drawing.Color.White;
            this.btnConvert.Location = new System.Drawing.Point(20, 397);
            this.btnConvert.Name = "btnConvert";
            this.btnConvert.Size = new System.Drawing.Size(356, 40);
            this.btnConvert.TabIndex = 2;
            this.btnConvert.Text = "Конвертировать";
            this.btnConvert.UseVisualStyleBackColor = false;
            this.btnConvert.Click += new System.EventHandler(this.BtnConvert_Click);
            // 
            // lblConvertTo
            // 
            this.lblConvertTo.AutoSize = true;
            this.lblConvertTo.Font = new System.Drawing.Font("Segoe UI", 14.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(204)));
            this.lblConvertTo.ForeColor = System.Drawing.Color.White;
            this.lblConvertTo.Location = new System.Drawing.Point(15, 20);
            this.lblConvertTo.Name = "lblConvertTo";
            this.lblConvertTo.Size = new System.Drawing.Size(183, 25);
            this.lblConvertTo.TabIndex = 1;
            this.lblConvertTo.Text = "Конвертировать в:";
            // 
            // lstConversionOptions
            // 
            this.lstConversionOptions.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(60)))), ((int)(((byte)(63)))), ((int)(((byte)(65)))));
            this.lstConversionOptions.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.lstConversionOptions.Font = new System.Drawing.Font("Segoe UI", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(204)));
            this.lstConversionOptions.ForeColor = System.Drawing.Color.White;
            this.lstConversionOptions.FormattingEnabled = true;
            this.lstConversionOptions.ItemHeight = 21;
            this.lstConversionOptions.Location = new System.Drawing.Point(20, 58);
            this.lstConversionOptions.Name = "lstConversionOptions";
            this.lstConversionOptions.Size = new System.Drawing.Size(356, 317);
            this.lstConversionOptions.TabIndex = 0;
            // 
            // Form1
            // 
            this.AllowDrop = true;
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(45)))), ((int)(((byte)(45)))), ((int)(((byte)(48)))));
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Controls.Add(this.splitContainer);
            this.Controls.Add(this.lblDragAndDrop);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;
            this.Name = "Form1";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Универсальный конвертер файлов";
            this.DragDrop += new System.Windows.Forms.DragEventHandler(this.Form1_DragDrop);
            this.DragEnter += new System.Windows.Forms.DragEventHandler(this.Form1_DragEnter);
            this.splitContainer.Panel1.ResumeLayout(false);
            this.splitContainer.Panel2.ResumeLayout(false);
            this.splitContainer.Panel2.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer)).EndInit();
            this.splitContainer.ResumeLayout(false);
            this.pnlFileInfo.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.picFileIcon)).EndInit();
            this.pnlConversionOptions.ResumeLayout(false);
            this.pnlConversionOptions.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Label lblDragAndDrop;
        private System.Windows.Forms.SplitContainer splitContainer;
        private System.Windows.Forms.Panel pnlFileInfo;
        private System.Windows.Forms.Panel pnlConversionOptions;
        private System.Windows.Forms.PictureBox picFileIcon;
        private System.Windows.Forms.Label lblFileName;
        private System.Windows.Forms.ListBox lstConversionOptions;
        private System.Windows.Forms.Label lblConvertTo;
        private System.Windows.Forms.Button btnConvert;
        private System.Windows.Forms.ProgressBar progressBar;
    }
}

//Help pls