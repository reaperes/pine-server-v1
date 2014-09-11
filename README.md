Version management
==================

v 1.0.6 latest version update.
---------------------------------
**Bug Fixed**

  * timeline/friends/since_offset API 
  * timeline/friends/previous_offset API 
  * comment push



### v 1.0.5.1
**Minor Update**
  
  * Minimum friend is now 2 (before 4) 

### v 1.0.5
**Update**
  
  * Add APIs
    
    get pine user list (POST: /friends/get)
    request authentication number (POST: /users/auth/request)
    
    
  * Update API
  
    register user (POST: /users/register)
    
        request
        {
            username:       (String),
            password:       (String),
            auth_num:       (String, authentication number),
            device_type:    (String, android or ios)
        }

        response
        {
            result:     (String, SUCCESS or FAIL),
            message:    (String, error message),
            auth_num:   (String, authentication number)
        }

### v 1.0.4
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
