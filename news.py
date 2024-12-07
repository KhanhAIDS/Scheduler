import feedparser
import json
import tkinter as tk
from tkinter import ttk
import webview

RSS_URL = "https://news.google.com/rss?hl=vi&gl=VN&ceid=VN:vi"


def fetch_vietnamese_news(file_name="vietnamese_news_rss.json"):
    try:
        feed = feedparser.parse(RSS_URL)

        if not feed.entries:
            print("[INFO] No articles found. Check the RSS URL.")
            return []
        
        articles = []
        for entry in feed.entries:
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.published
            })
            
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(articles, f, ensure_ascii=False, indent=4)

        print(f"[INFO] Vietnamese news articles saved to '{file_name}'.")
        return articles
    except Exception as e:
        print(f"[ERROR] An error occurred while fetching news: {e}")
        return []


def display_article_in_browser_frame(root, main_frame, article_url):
    
    for widget in main_frame.winfo_children():
        widget.destroy()

    loading_label = ttk.Label(main_frame, text="Loading article...", font=("Arial", 14))
    loading_label.pack(pady=20)

    def start_webview():
        loading_label.destroy()
        webview.create_window("Article Viewer", article_url)
        webview.start()

    root.after(100, start_webview)

    back_button = ttk.Button(main_frame, text="Back", command=lambda: show_main_menu(root, main_frame))
    back_button.pack(pady=10)


def show_main_menu(root, main_frame):
    
    for widget in main_frame.winfo_children():
        widget.destroy()

    file_name = "vietnamese_news_rss.json"
    articles = fetch_vietnamese_news(file_name)

    canvas = tk.Canvas(main_frame)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    row = 0
    col = 0
    for article in articles:
        article_button = tk.Button(
            scrollable_frame,
            text=f"{article['title']} ({article['published']})",
            command=lambda a=article: display_article_in_browser_frame(root, main_frame, a["link"]),
            wraplength=300,
            font=("Arial", 10),
            justify="center",
            padx=10,
            pady=10
        )
        article_button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        scrollable_frame.grid_columnconfigure(col, weight=1)

        col += 1
        if col >= 2:
            col = 0
            row += 1

def display_news_ui():
    root = tk.Tk()
    root.title("Vietnamese News")
    root.geometry("800x600")

    main_frame = ttk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    show_main_menu(root, main_frame)

    root.mainloop()

if __name__ == "__main__":
    display_news_ui()