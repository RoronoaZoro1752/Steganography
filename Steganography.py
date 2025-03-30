from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np

class ImageSteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Steganography")
        self.root.geometry("800x600")
        
       
        self.original_image = None
        self.modified_image = None
        self.message = tk.StringVar()
        
        
        self.setup_ui()
    
    def setup_ui(self):
        
        image_frame = tk.Frame(self.root)
        image_frame.pack(pady=10)
        
        
        self.original_label = tk.Label(image_frame, text="Original Image", relief=tk.SUNKEN)
        self.original_label.pack(side=tk.LEFT, padx=10)
        
        
        self.modified_label = tk.Label(image_frame, text="Modified Image", relief=tk.SUNKEN)
        self.modified_label.pack(side=tk.RIGHT, padx=10)
        
        
        message_frame = tk.Frame(self.root)
        message_frame.pack(pady=10)
        
        tk.Label(message_frame, text="Secret Message:").pack(side=tk.LEFT)
        self.message_entry = tk.Entry(message_frame, textvariable=self.message, width=50)
        self.message_entry.pack(side=tk.LEFT, padx=5)
        
        
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Load Image", command=self.load_image).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Encode", command=self.encode_message).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Decode", command=self.decode_message).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Save Image", command=self.save_image).pack(side=tk.LEFT, padx=5)
    
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.display_image(self.original_image, self.original_label)
                self.modified_image = None
                self.modified_label.config(image='')
                self.modified_label.image = None
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def display_image(self, image, label):
        
        width, height = image.size
        ratio = min(300/width, 300/height)
        new_size = (int(width * ratio), int(height * ratio))
        resized_image = image.resize(new_size)
        
        photo = ImageTk.PhotoImage(resized_image)
        label.config(image=photo)
        label.image = photo
    
    def encode_message(self):
        if not self.original_image:
            messagebox.showerror("Error", "Please load an image first")
            return
        
        message = self.message.get().strip()
        if not message:
            messagebox.showerror("Error", "Please enter a message to encode")
            return
        
        try:
            
            img = self.original_image.convert("RGB")
            pixels = np.array(img)
            
            
            message += "%%%"
            binary_message = ''.join([format(ord(c), '08b') for c in message])
            
            if len(binary_message) > pixels.size:
                messagebox.showerror("Error", "Message too large for the image")
                return
            
            
            idx = 0
            for i in range(pixels.shape[0]):
                for j in range(pixels.shape[1]):
                    for k in range(3):  
                        if idx < len(binary_message):
                            pixels[i][j][k] = pixels[i][j][k] & ~1 | int(binary_message[idx])
                            idx += 1
            
            self.modified_image = Image.fromarray(pixels)
            self.display_image(self.modified_image, self.modified_label)
            messagebox.showinfo("Success", "Message encoded successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to encode message: {str(e)}")
    
    def decode_message(self):
        if not self.original_image:
            messagebox.showerror("Error", "Please load an image first")
            return
        
        try:
            img = self.original_image.convert("RGB")
            pixels = np.array(img)
            
            binary_message = []
            for i in range(pixels.shape[0]):
                for j in range(pixels.shape[1]):
                    for k in range(3):  
                        binary_message.append(str(pixels[i][j][k] & 1))
            
            
            message = ""
            for i in range(0, len(binary_message), 8):
                byte = binary_message[i:i+8]
                if len(byte) < 8:
                    break
                char = chr(int(''.join(byte), 2))
                message += char
                
                if message[-3:] == "%%%":
                    message = message[:-3]
                    self.message.set(message)
                    messagebox.showinfo("Decoded Message", f"Decoded message: {message}")
                    return
            
            messagebox.showinfo("Result", "No hidden message found or message incomplete")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to decode message: {str(e)}")
    
    def save_image(self):
        if not self.modified_image:
            messagebox.showerror("Error", "No modified image to save")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".png", 
                                                filetypes=[("PNG files", "*.png"), 
                                                           ("JPEG files", "*.jpg")])
        if file_path:
            try:
                self.modified_image.save(file_path)
                messagebox.showinfo("Success", "Image saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSteganographyApp(root)
    root.mainloop()