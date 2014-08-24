Version management
==================

v 1.0.1 latest version update.
-----------------------
**Update**
  * add event_date in ios push message. (need to test)
  * add `image_url` key in ios push json.
  
        "aps": {
            "alert": (message, String),
            "badge": 1,
        },
        'thread_id': (int),
        'event_date': 'YYYY-mm-dd HH:MM:SS',
        'image_url': (String)

**Bug fixed**
  * thread, comment notification error.
