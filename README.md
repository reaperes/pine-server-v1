Version management
==================


v 1.0.4 latest version update.
------------------------------
**Deprecate**
  * API /threads/<thread_id>/offset?is_friend={boolean}

**Update**
  * add `view_count` key in thread, timeline APIs.

        Examples
        {
            id:           (Number, Threads.id),
            type:         (Number, 0-none 1-author),
            like_count:   (Number, how many users like),
            view_count:   (Number, how many users view),
            liked:        (Boolean, if user like or not),
            pub_date:     (String, '%Y-%m-%d %H:%M:%S'),
            image_url:    (String, image url here),
            content:      (String, content <= 200),
            comment:      (Number, how many comments commented)
        },

        Updated Apis
        Get latest timeline                                      [/timeline/friends?count={count}]
        Get next threads in timeline starting from offset thread [/timeline/friends/since_offset?offset_id={offset_id}&count={count}]
        Get friend's timeline previous offset                    [/timeline/friends/previous_offset?offset_id={offset_id}&count={count}]      
        Get thread                                               [/threads/<thread_id>]


### v 1.0.3
**Update**
  * apply django 1.7
  * apply request 2.4


### v 1.0.2 update 
**Update**
  * add `type` key in thread APIs.
        
        Examples
        {
            id:           (Number, Threads.id),
            type:         (Number, 0-none 1-author),
            like_count:   (Number, how many users like),
            liked:        (Boolean, if user like or not),
            pub_date:     (String, '%Y-%m-%d %H:%M:%S'),
            image_url:    (String, image url here),
            content:      (String, content <= 200),
            comment:      (Number, how many comments commented)
        },

        Updated apis
        Get latest timeline                                      [/timeline/friends?count={count}]
        Get next threads in timeline starting from offset thread [/timeline/friends/since_offset?offset_id={offset_id}&count={count}]
        Get friend's timeline previous offset                    [/timeline/friends/previous_offset?offset_id={offset_id}&count={count}]      
        Get thread                                               [/threads/<thread_id>]


### v 1.0.1 update.
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
