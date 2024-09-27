import tkinter as tk
from tkinter import filedialog

class HomepageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Homepage")
        self.is_data_uploading = False
        self.uploaded_local_files = []
        self.uploaded_file_urls = []

        self.create_widgets()

    def create_widgets(self):
        self.root.geometry("800x600")

        # Create a label for the image
        image_label = tk.Label(self.root)
        
        

        image_label.pack(fill=tk.BOTH, expand=True)

        # Load and display an image
        image_path = "assets/images/WhatsApp_Image_2023-11-03_at_13.29.12_c5f877f2.jpg"
        image = tk.PhotoImage(file=image_path)
        image_label.config(image=image)
        image_label.image = image

        # Create an "Upload Notes" button
        upload_button = tk.Button(self.root, text="Upload Notes", command=self.upload_notes)
        upload_button.pack(pady=10)

        # Create a label for uploaded files
        uploaded_files_label = tk.Label(self.root, text="Uploaded Files:")
        uploaded_files_label.pack()

        self.uploaded_files_text = tk.Text(self.root, height=5, width=40)
        self.uploaded_files_text.pack()

    def upload_notes(self):
        if self.is_data_uploading:
            return

        selected_files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        if selected_files:
            self.is_data_uploading = True
            self.update_upload_status("Uploading file...")

            # Simulate uploading and update the uploaded files and URLs
            self.uploaded_local_files.extend(selected_files)
            self.uploaded_file_urls.extend(["https://example.com/file1.pdf", "https://example.com/file2.pdf"])

            self.update_upload_status("Success!")

    def update_upload_status(self, message):
        self.uploaded_files_text.delete(1.0, tk.END)
        self.uploaded_files_text.insert(tk.END, message)
        self.is_data_uploading = False

if __name__ == "__main__":
    root = tk.Tk()
    app = HomepageApp(root)
    root.mainloop()