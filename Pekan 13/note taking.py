import customtkinter as ctk
from tkinter import messagebox
from collections import deque


# ==========================================
# NOTE CLASS
# ==========================================
class Note:
    def __init__(self, note_id, title, content):
        self.note_id = note_id
        self.title = title
        self.content = content
        self.tags = []

    def add_tag(self, tag):
        self.tags.append(tag)


# ==========================================
# TAG CLASS
# ==========================================
class Tag:
    def __init__(self, name):
        self.name = name
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)


# ==========================================
# CIRCULAR BUFFER
# ==========================================
class CircularBuffer:
    def __init__(self, size):
        self.buffer = deque(maxlen=size)

    def add_change(self, change):
        self.buffer.append(change)

    def get_changes(self):
        return list(self.buffer)


# ==========================================
# MAIN APP
# ==========================================
class NoteApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Modern Notes")
        self.root.geometry("1000x650")
        self.root.minsize(900, 600)

        # THEME
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # DATA
        self.notes = []
        self.tags = {}
        self.sync_buffer = CircularBuffer(5)

        # UI
        self.create_layout()

    # ======================================
    # UI LAYOUT
    # ======================================
    def create_layout(self):

        # MAIN CONTAINER
        self.container = ctk.CTkFrame(
            self.root,
            fg_color="#0f0f0f"
        )
        self.container.pack(fill="both", expand=True, padx=15, pady=15)

        # ==================================
        # LEFT PANEL
        # ==================================
        self.left_panel = ctk.CTkFrame(
            self.container,
            width=320,
            fg_color="#171717",
            corner_radius=15
        )
        self.left_panel.pack(side="left", fill="y", padx=(0, 10))

        # TITLE
        title = ctk.CTkLabel(
            self.left_panel,
            text="📝 Modern Notes",
            font=("Segoe UI", 28, "bold")
        )
        title.pack(pady=(25, 20))

        # TITLE INPUT
        self.title_entry = ctk.CTkEntry(
            self.left_panel,
            placeholder_text="Note title",
            height=45,
            corner_radius=10
        )
        self.title_entry.pack(fill="x", padx=20, pady=10)

        # CONTENT
        self.content_box = ctk.CTkTextbox(
            self.left_panel,
            height=180,
            corner_radius=10
        )
        self.content_box.pack(fill="x", padx=20, pady=10)

        # TAG INPUT
        self.tag_entry = ctk.CTkEntry(
            self.left_panel,
            placeholder_text="Tags (comma separated)",
            height=45,
            corner_radius=10
        )
        self.tag_entry.pack(fill="x", padx=20, pady=10)

        # ADD BUTTON
        add_btn = ctk.CTkButton(
            self.left_panel,
            text="Add Note",
            height=45,
            corner_radius=12,
            font=("Segoe UI", 15, "bold"),
            command=self.add_note
        )
        add_btn.pack(fill="x", padx=20, pady=(15, 10))

        # VIEW BUTTONS
        sort_alpha_btn = ctk.CTkButton(
            self.left_panel,
            text="Alphabetical",
            fg_color="#262626",
            hover_color="#333333",
            command=self.show_alphabetical
        )
        sort_alpha_btn.pack(fill="x", padx=20, pady=5)

        sort_chrono_btn = ctk.CTkButton(
            self.left_panel,
            text="Chronological",
            fg_color="#262626",
            hover_color="#333333",
            command=self.show_chronological
        )
        sort_chrono_btn.pack(fill="x", padx=20, pady=5)

        sync_btn = ctk.CTkButton(
            self.left_panel,
            text="Recent Sync",
            fg_color="#262626",
            hover_color="#333333",
            command=self.show_sync
        )
        sync_btn.pack(fill="x", padx=20, pady=5)

        # ==================================
        # RIGHT PANEL
        # ==================================
        self.right_panel = ctk.CTkFrame(
            self.container,
            fg_color="#121212",
            corner_radius=15
        )
        self.right_panel.pack(side="right", fill="both", expand=True)

        notes_label = ctk.CTkLabel(
            self.right_panel,
            text="All Notes",
            font=("Segoe UI", 24, "bold")
        )
        notes_label.pack(anchor="w", padx=20, pady=(20, 10))

        # SCROLLABLE FRAME
        self.notes_frame = ctk.CTkScrollableFrame(
            self.right_panel,
            fg_color="#121212"
        )
        self.notes_frame.pack(fill="both", expand=True, padx=15, pady=10)

    # ======================================
    # ADD NOTE
    # ======================================
    def add_note(self):

        title = self.title_entry.get().strip()
        content = self.content_box.get("1.0", "end").strip()
        tag_text = self.tag_entry.get().strip()

        if not title or not content:
            messagebox.showerror(
                "Error",
                "Title and content cannot be empty"
            )
            return

        note = Note(
            len(self.notes) + 1,
            title,
            content
        )

        tags = [
            tag.strip()
            for tag in tag_text.split(",")
            if tag.strip()
        ]

        for tag_name in tags:

            if tag_name not in self.tags:
                self.tags[tag_name] = Tag(tag_name)

            note.add_tag(tag_name)
            self.tags[tag_name].add_note(note)

        self.notes.append(note)

        self.sync_buffer.add_change(
            f"Added note: {title}"
        )

        self.render_notes(self.notes)

        # CLEAR INPUTS
        self.title_entry.delete(0, "end")
        self.content_box.delete("1.0", "end")
        self.tag_entry.delete(0, "end")

    # ======================================
    # RENDER NOTES
    # ======================================
    def render_notes(self, notes):

        # CLEAR OLD NOTES
        for widget in self.notes_frame.winfo_children():
            widget.destroy()

        # CREATE NOTE CARDS
        for note in notes:

            card = ctk.CTkFrame(
                self.notes_frame,
                fg_color="#1b1b1b",
                corner_radius=15
            )
            card.pack(fill="x", pady=10, padx=5)

            # TITLE
            title = ctk.CTkLabel(
                card,
                text=note.title,
                font=("Segoe UI", 20, "bold")
            )
            title.pack(anchor="w", padx=15, pady=(15, 5))

            # CONTENT
            content = ctk.CTkLabel(
                card,
                text=note.content,
                justify="left",
                wraplength=550,
                text_color="#cfcfcf"
            )
            content.pack(anchor="w", padx=15)

            # TAGS
            tags = ", ".join(note.tags)

            tag_label = ctk.CTkLabel(
                card,
                text=f"🏷 {tags}",
                text_color="#7f8cff"
            )
            tag_label.pack(anchor="w", padx=15, pady=(10, 15))

    # ======================================
    # SORT ALPHABETICAL
    # ======================================
    def show_alphabetical(self):

        sorted_notes = sorted(
            self.notes,
            key=lambda note: note.title.lower()
        )

        self.render_notes(sorted_notes)

    # ======================================
    # SORT CHRONOLOGICAL
    # ======================================
    def show_chronological(self):
        self.render_notes(self.notes)

    # ======================================
    # SHOW SYNC BUFFER
    # ======================================
    def show_sync(self):

        changes = self.sync_buffer.get_changes()

        if not changes:
            message = "No recent changes"
        else:
            message = "\n".join(changes)

        messagebox.showinfo(
            "Recent Sync Changes",
            message
        )


# ==========================================
# RUN APP
# ==========================================
if __name__ == "__main__":

    root = ctk.CTk()

    app = NoteApp(root)

    root.mainloop()