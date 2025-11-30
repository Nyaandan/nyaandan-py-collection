cursors = [
        "arrow", "circle", "clock", "cross", "dotbox", "exchange", "fleur", "heart",
        "man", "mouse", "pirate", "plus", "shuttle", "sizing", "spider", "spraycan",
        "star", "target", "tcross", "trek"
        ]

    for cursor in cursors:
        tk.Button(debug_frame, text=cursor, cursor=cursor).pack(side="left", padx=2, pady=2)