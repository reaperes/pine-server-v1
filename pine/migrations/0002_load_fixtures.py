# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


sql = [
"SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT;",
"SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS;",
"SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION;",
"SET NAMES utf8;",
"SET @OLD_TIME_ZONE=@@TIME_ZONE;",
"SET TIME_ZONE='+00:00';",
"SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;",
"SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;",
"SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO';",
"SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0;",
"DROP TABLE IF EXISTS auth_group;",
"SET @saved_cs_client     = @@character_set_client;",
"SET character_set_client = utf8;",
"CREATE TABLE auth_group ("
"  id int(11) NOT NULL AUTO_INCREMENT,"
"  name varchar(80) NOT NULL,"
"  PRIMARY KEY (id),"
"  UNIQUE KEY name (name)"
") ENGINE=InnoDB DEFAULT CHARSET=utf8;",
"SET character_set_client = @saved_cs_client;",
"LOCK TABLES auth_group WRITE;",
"ALTER TABLE auth_group DISABLE KEYS;",
"ALTER TABLE auth_group ENABLE KEYS;",
"UNLOCK TABLES;",
"DROP TABLE IF EXISTS auth_group_permissions;",
"SET @saved_cs_client     = @@character_set_client;",
"SET character_set_client = utf8;",
"CREATE TABLE auth_group_permissions ("
"  id int(11) NOT NULL AUTO_INCREMENT,"
"  group_id int(11) NOT NULL,"
"  permission_id int(11) NOT NULL,"
"  PRIMARY KEY (id),"
"  UNIQUE KEY group_id (group_id,permission_id),"
"  KEY auth_group_permissions_0e939a4f (group_id),"
"  KEY auth_group_permissions_8373b171 (permission_id),"
"  CONSTRAINT auth_group_pe_permission_id_a2e7bba7216ff7_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission (id),"
"  CONSTRAINT auth_group_permission_group_id_4089d5d4d7c1a949_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group (id)"
") ENGINE=InnoDB DEFAULT CHARSET=utf8;",
"SET character_set_client = @saved_cs_client;",
"LOCK TABLES auth_group_permissions WRITE;",
"ALTER TABLE auth_group_permissions DISABLE KEYS;",
"ALTER TABLE auth_group_permissions ENABLE KEYS;",
"UNLOCK TABLES;",
"DROP TABLE IF EXISTS auth_permission;",
"SET @saved_cs_client     = @@character_set_client;",
"SET character_set_client = utf8;",
"CREATE TABLE auth_permission ("
"  id int(11) NOT NULL AUTO_INCREMENT,"
"  name varchar(50) NOT NULL,"
"  content_type_id int(11) NOT NULL,"
"  codename varchar(100) NOT NULL,"
"  PRIMARY KEY (id),"
"  UNIQUE KEY content_type_id (content_type_id,codename),"
"  KEY auth_permission_417f1b1c (content_type_id),"
"  CONSTRAINT auth__content_type_id_4fb93b97250b2c27_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type (id)"
") ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;",
"SET character_set_client = @saved_cs_client;",
"LOCK TABLES auth_permission WRITE;",
"ALTER TABLE auth_permission DISABLE KEYS;",
"INSERT INTO auth_permission VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add phones',7,'add_phones'),(20,'Can change phones',7,'change_phones'),(21,'Can delete phones',7,'delete_phones'),(22,'Can add users',8,'add_users'),(23,'Can change users',8,'change_users'),(24,'Can delete users',8,'delete_users'),(25,'Can add threads',9,'add_threads'),(26,'Can change threads',9,'change_threads'),(27,'Can delete threads',9,'delete_threads'),(28,'Can add comments',10,'add_comments'),(29,'Can change comments',10,'change_comments'),(30,'Can delete comments',10,'delete_comments');",
"ALTER TABLE auth_permission ENABLE KEYS;",
"UNLOCK TABLES;",
"DROP TABLE IF EXISTS auth_user;",
"SET @saved_cs_client     = @@character_set_client;",
"SET character_set_client = utf8;",
"CREATE TABLE auth_user ("
"  id int(11) NOT NULL AUTO_INCREMENT,"
"  password varchar(128) NOT NULL,"
"  last_login datetime NOT NULL,"
"  is_superuser tinyint(1) NOT NULL,"
"  username varchar(30) NOT NULL,"
"  first_name varchar(30) NOT NULL,"
"  last_name varchar(30) NOT NULL,"
"  email varchar(75) NOT NULL,"
"  is_staff tinyint(1) NOT NULL,"
"  is_active tinyint(1) NOT NULL,"
"  date_joined datetime NOT NULL,"
"  PRIMARY KEY (id),"
"  UNIQUE KEY username (username)"
") ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;",
"SET character_set_client = @saved_cs_client;",
"LOCK TABLES auth_user WRITE;",
"ALTER TABLE auth_user DISABLE KEYS;",
"INSERT INTO auth_user VALUES (1,'pbkdf2_sha256$12000$tGQyY9GZEAdK$XRVF89JR08p1nDMZHtW7oboFR/QBu+HPGjHgc+ViY50=','2014-09-03 13:58:33',0,'01032080403','','','',0,1,'2014-09-03 13:58:33'),(2,'pbkdf2_sha256$12000$5j1JgtXTctvi$7kjTpkJxaN9QNv284znZk107r+EBi8kQRCL7dl6qi8U=','2014-09-03 13:58:33',0,'01098590530','','','',0,1,'2014-09-03 13:58:33'),(3,'pbkdf2_sha256$12000$aLZWPLqrhhog$IrRvZoolnkGkf2ETEkbHIGlsStednB/nWJAOR1bhIJM=','2014-09-03 13:58:33',0,'01087537711','','','',0,1,'2014-09-03 13:58:33'),(4,'pbkdf2_sha256$12000$GfKcTLnKbbxH$vFeD217URuUd6UoEBpyO51HB5eMeCfpGCGBqM01pA7Q=','2014-09-03 13:58:33',0,'01021101783','','','',0,1,'2014-09-03 13:58:33'),(5,'pbkdf2_sha256$12000$IK3q5GpLBBFD$eoHtTaD/7JmueXZeNJLRKEPOBlcDuKEVkQR+3age/JE=','2014-09-03 13:58:33',0,'01040099179','','','',0,1,'2014-09-03 13:58:33'),(6,'pbkdf2_sha256$12000$AKterSZxVwMi$wAqun/ijfrVwoNijuAMXqfUlERVhKb06NNkjosYMO3M=','2014-09-03 13:58:33',0,'01089607165','','','',0,1,'2014-09-03 13:58:33'),(7,'pbkdf2_sha256$12000$uqZSeowDeZ4a$mh/q20d3+x9RmvRq+crA0TmY90C4afWiyEMHmTwZj+Y=','2014-09-03 13:58:33',0,'01037585989','','','',0,1,'2014-09-03 13:58:33'),(8,'pbkdf2_sha256$12000$NpHE2KM6alSU$YQzeciGQfoJKu+jy0x2PEnJzayXgiBlNGxq5MxOj/mk=','2014-09-03 13:58:33',0,'01020624493','','','',0,1,'2014-09-03 13:58:33'),(9,'pbkdf2_sha256$12000$iqBQweNoB59u$aZJm2mYg924YFo/gcgOZAD2EQUIivf8nAvK3haeVVco=','2014-09-03 13:58:33',0,'01020863441','','','',0,1,'2014-09-03 13:58:33'),(10,'pbkdf2_sha256$12000$kFW0pCZ4trad$brBG4Niz7dGLQ6lFwY7uuh8G32N8ZdHw/BBmtAN8JKk=','2014-09-03 13:58:33',0,'01092696960','','','',0,1,'2014-09-03 13:58:33');",
"ALTER TABLE auth_user ENABLE KEYS;",
"UNLOCK TABLES;",
"DROP TABLE IF EXISTS auth_user_groups;",
"SET @saved_cs_client     = @@character_set_client;",
"SET character_set_client = utf8;",
"CREATE TABLE auth_user_groups ("
"  id int(11) NOT NULL AUTO_INCREMENT,"
"  user_id int(11) NOT NULL,"
"  group_id int(11) NOT NULL,"
"  PRIMARY KEY (id),"
"  UNIQUE KEY user_id (user_id,group_id),"
"  KEY auth_user_groups_e8701ad4 (user_id),"
"  KEY auth_user_groups_0e939a4f (group_id),"
"  CONSTRAINT auth_user_groups_group_id_21c2b36faa3c8cae_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group (id),"
"  CONSTRAINT auth_user_groups_user_id_54ca3847a831d5cf_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user (id)"
") ENGINE=InnoDB DEFAULT CHARSET=utf8;",
"SET character_set_client = @saved_cs_client;",
"LOCK TABLES auth_user_groups WRITE;",
"ALTER TABLE auth_user_groups DISABLE KEYS;",
"ALTER TABLE auth_user_groups ENABLE KEYS;",
"UNLOCK TABLES;",
"DROP TABLE IF EXISTS auth_user_user_permissions;",
"SET @saved_cs_client     = @@character_set_client;",
"SET character_set_client = utf8;",
"CREATE TABLE auth_user_user_permissions ("
"  id int(11) NOT NULL AUTO_INCREMENT,"
"  user_id int(11) NOT NULL,"
"  permission_id int(11) NOT NULL,"
"  PRIMARY KEY (id),"
"  UNIQUE KEY user_id (user_id,permission_id),"
"  KEY auth_user_user_permissions_e8701ad4 (user_id),"
"  KEY auth_user_user_permissions_8373b171 (permission_id),"
"  CONSTRAINT auth_user_u_permission_id_252d31d2e6acd566_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission (id),"
"  CONSTRAINT auth_user_user_permissi_user_id_6cd07a0e9f0244fb_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user (id)"
") ENGINE=InnoDB DEFAULT CHARSET=utf8;",
"SET character_set_client = @saved_cs_client;",
"LOCK TABLES auth_user_user_permissions WRITE;",
"ALTER TABLE auth_user_user_permissions DISABLE KEYS;",
"ALTER TABLE auth_user_user_permissions ENABLE KEYS;",
"UNLOCK TABLES;",
"DROP TABLE IF EXISTS django_admin_log;",
"SET @saved_cs_client     = @@character_set_client;",
"SET character_set_client = utf8;",
"CREATE TABLE django_admin_log ("
"  id int(11) NOT NULL AUTO_INCREMENT,"
"  action_time datetime NOT NULL,"
"  object_id longtext,"
"  object_repr varchar(200) NOT NULL,"
"  action_flag smallint(5) unsigned NOT NULL,"
"  change_message longtext NOT NULL,"
"  content_type_id int(11) DEFAULT NULL,"
"  user_id int(11) NOT NULL,"
"  PRIMARY KEY (id),"
"  KEY django_admin_log_417f1b1c (content_type_id),"
"  KEY django_admin_log_e8701ad4 (user_id),"
"  CONSTRAINT django_admin_log_user_id_18e0d6cbf69c1395_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user (id),"
"  CONSTRAINT django_content_type_id_bc99eb2465d3000_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type (id)"
") ENGINE=InnoDB DEFAULT CHARSET=utf8;",
"SET character_set_client = @saved_cs_client;",
"LOCK TABLES django_admin_log WRITE;",
"ALTER TABLE django_admin_log DISABLE KEYS;",
"ALTER TABLE django_admin_log ENABLE KEYS;",
"UNLOCK TABLES;",
"DROP TABLE IF EXISTS django_content_type;",
"SET @saved_cs_client     = @@character_set_client;",
"SET character_set_client = utf8;",
"CREATE TABLE django_content_type ("
"  id int(11) NOT NULL AUTO_INCREMENT,"
"  name varchar(100) NOT NULL,"
"  app_label varchar(100) NOT NULL,"
"  model varchar(100) NOT NULL,"
"  PRIMARY KEY (id),"
"  UNIQUE KEY django_content_type_app_label_17fa928a07628026_uniq (app_label,model)"
") ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;",
"SET character_set_client = @saved_cs_client;",
"LOCK TABLES django_content_type WRITE;",
"ALTER TABLE django_content_type DISABLE KEYS;",
"INSERT INTO django_content_type VALUES (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group'),(4,'user','auth','user'),(5,'content type','contenttypes','contenttype'),(6,'session','sessions','session'),(7,'phones','pine','phones'),(8,'users','pine','users'),(9,'threads','pine','threads'),(10,'comments','pine','comments');",
"ALTER TABLE django_content_type ENABLE KEYS;",
"UNLOCK TABLES;",
"DROP TABLE IF EXISTS django_migrations;",
"SET @saved_cs_client     = @@character_set_client;",
"SET character_set_client = utf8;",
"CREATE TABLE django_migrations ("
"  id int(11) NOT NULL AUTO_INCREMENT,"
"  app varchar(255) NOT NULL,"
"  name varchar(255) NOT NULL,"
"  applied datetime NOT NULL,"
"  PRIMARY KEY (id)"
") ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;",
"SET character_set_client = @saved_cs_client;",
"LOCK TABLES django_migrations WRITE;",
"ALTER TABLE django_migrations DISABLE KEYS;",
"INSERT INTO django_migrations VALUES (1,'contenttypes','0001_initial','2014-09-03 13:57:34'),(2,'auth','0001_initial','2014-09-03 13:57:36'),(3,'admin','0001_initial','2014-09-03 13:57:37'),(4,'pine','0001_initial','2014-09-03 13:57:43'),(5,'pine','0002_load_fixtures','2014-09-03 13:57:43'),(6,'sessions','0001_initial','2014-09-03 13:57:43');",
"ALTER TABLE django_migrations ENABLE KEYS;",
"UNLOCK TABLES;",
"DROP TABLE IF EXISTS django_session;",
"SET @saved_cs_client     = @@character_set_client;",
"SET character_set_client = utf8;",
"CREATE TABLE django_session ("
"  session_key varchar(40) NOT NULL,"
"  session_data longtext NOT NULL,"
"  expire_date datetime NOT NULL,"
"  PRIMARY KEY (session_key),"
"  KEY django_session_de54fa62 (expire_date)"
") ENGINE=InnoDB DEFAULT CHARSET=utf8;",
"SET character_set_client = @saved_cs_client;",
"LOCK TABLES django_session WRITE;",
"ALTER TABLE django_session DISABLE KEYS;",
"ALTER TABLE django_session ENABLE KEYS;",
"UNLOCK TABLES;",
"DROP TABLE IF EXISTS pine_comments;",
"SET @saved_cs_client     = @@character_set_client;",
"SET character_set_client = utf8;",
"CREATE TABLE pine_comments ("
"  id int(11) NOT NULL AUTO_INCREMENT,"
"  max_like int(11) NOT NULL,"
"  pub_date datetime NOT NULL,"
"  content varchar(500) NOT NULL,"
"  author_id int(11) NOT NULL,"
"  thread_id int(11) NOT NULL,"
"  PRIMARY KEY (id),"
"  KEY pine_comments_4f331e2f (author_id),"
"  KEY pine_comments_e3464c97 (thread_id),"
"  CONSTRAINT pine_comments_thread_id_79ff60eee9f88467_fk_pine_threads_id FOREIGN KEY (thread_id) REFERENCES pine_threads (id),"
"  CONSTRAINT pine_comments_author_id_214c5a130c1e1e46_fk_pine_users_id FOREIGN KEY (author_id) REFERENCES pine_users (id)"
") ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;",
"SET character_set_client = @saved_cs_client;",
"LOCK TABLES pine_comments WRITE;",
"ALTER TABLE pine_comments DISABLE KEYS;",
"INSERT INTO pine_comments VALUES (1,0,'2014-06-01 00:00:01','Namhoons first comment.',1,1),(2,0,'2014-06-01 00:00:02','랄랄라 ^-^',8,1),(3,0,'2014-06-01 00:00:03','hello',4,1),(4,0,'2014-06-19 17:45:39','comment',1,8);",
"ALTER TABLE pine_comments ENABLE KEYS;",
"UNLOCK TABLES;",
"DROP TABLE IF EXISTS pine_comments_likes;",
"SET @saved_cs_client     = @@character_set_client;",
"SET character_set_client = utf8;",
"CREATE TABLE pine_comments_likes ("
"  id int(11) NOT NULL AUTO_INCREMENT,"
"  comments_id int(11) NOT NULL,"
"  users_id int(11) NOT NULL,"
"  PRIMARY KEY (id),"
"  UNIQUE KEY comments_id (comments_id,users_id),"
"  KEY pine_comments_likes_e7131757 (comments_id),"
"  KEY pine_comments_likes_df138c17 (users_id),"
"  CONSTRAINT pine_comments_likes_users_id_189e6c951688b873_fk_pine_users_id FOREIGN KEY (users_id) REFERENCES pine_users (id),"
"  CONSTRAINT pine_comments_l_comments_id_5697188e2e586e2e_fk_pine_comments_id FOREIGN KEY (comments_id) REFERENCES pine_comments (id)"
") ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;",
"SET character_set_client = @saved_cs_client;",
"LOCK TABLES pine_comments_likes WRITE;",
"ALTER TABLE pine_comments_likes DISABLE KEYS;",
"INSERT INTO pine_comments_likes VALUES (1,1,1),(2,1,2),(3,1,3);",
"ALTER TABLE pine_comments_likes ENABLE KEYS;",
"UNLOCK TABLES;",
"DROP TABLE IF EXISTS pine_comments_reports;",
"SET @saved_cs_client     = @@character_set_client;",
"SET character_set_client = utf8;",
"CREATE TABLE pine_comments_reports ("
"  id int(11) NOT NULL AUTO_INCREMENT,"
"  comments_id int(11) NOT NULL,"
"  users_id int(11) NOT NULL,"
"  PRIMARY KEY (id),"
"  UNIQUE KEY comments_id (comments_id,users_id),"
"  KEY pine_comments_reports_e7131757 (comments_id),"
"  KEY pine_comments_reports_df138c17 (users_id),"
"  CONSTRAINT pine_comments_reports_users_id_1577a3fa6df94c94_fk_pine_users_id FOREIGN KEY (users_id) REFERENCES pine_users (id),"
"  CONSTRAINT pine_comments_r_comments_id_69e3cf745eb350a5_fk_pine_comments_id FOREIGN KEY (comments_id) REFERENCES pine_comments (id)"
") ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;",
"SET character_set_client = @saved_cs_client;",
"LOCK TABLES pine_comments_reports WRITE;",
"ALTER TABLE pine_comments_reports DISABLE KEYS;",
"INSERT INTO pine_comments_reports VALUES (1,1,4);",
"ALTER TABLE pine_comments_reports ENABLE KEYS;",
"UNLOCK TABLES;",
"DROP TABLE IF EXISTS pine_phones;",
"SET @saved_cs_client     = @@character_set_client;",
"SET character_set_client = utf8;",
"CREATE TABLE pine_phones ("
"  id int(11) NOT NULL AUTO_INCREMENT,"
"  phone_number varchar(15) NOT NULL,"
"  PRIMARY KEY (id),"
"  UNIQUE KEY phone_number (phone_number)"
") ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;",
"SET character_set_client = @saved_cs_client;",
"LOCK TABLES pine_phones WRITE;",
"ALTER TABLE pine_phones DISABLE KEYS;",
"INSERT INTO pine_phones VALUES (8,'01020624493'),(9,'01020863441'),(4,'01021101783'),(11,'01026969960'),(1,'01032080403'),(7,'01037585989'),(5,'01040099179'),(10,'01085174557'),(3,'01087537711'),(6,'01089607165'),(2,'01098590530');",
"ALTER TABLE pine_phones ENABLE KEYS;",
"UNLOCK TABLES;",
"DROP TABLE IF EXISTS pine_threads;",
"SET @saved_cs_client     = @@character_set_client;",
"SET character_set_client = utf8;",
"CREATE TABLE pine_threads ("
"  id int(11) NOT NULL AUTO_INCREMENT,"
"  is_public tinyint(1) NOT NULL,"
"  max_like int(11) NOT NULL,"
"  pub_date datetime NOT NULL,"
"  image_url varchar(256) NOT NULL,"
"  content varchar(1000) NOT NULL,"
"  author_id int(11) NOT NULL,"
"  PRIMARY KEY (id),"
"  KEY pine_threads_4f331e2f (author_id),"
"  CONSTRAINT pine_threads_author_id_6e851ff8f9b9fa7e_fk_pine_users_id FOREIGN KEY (author_id) REFERENCES pine_users (id)"
") ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;",
"SET character_set_client = @saved_cs_client;",
"LOCK TABLES pine_threads WRITE;",
"ALTER TABLE pine_threads DISABLE KEYS;",
"INSERT INTO pine_threads VALUES (1,0,0,'2014-06-01 00:00:00','test_image.png','Im Namhoon. This threads can be viewed only my friends Sujin, Hanyong, etc.',1),(2,1,0,'2014-06-01 00:00:01','test_image.png','Im Namhoon. This threads can be viewed anyone.',1),(3,0,0,'2014-06-01 00:04:00','test_image.png','Im pf. Choi. Its friends thread.',6),(4,1,0,'2014-06-01 01:24:50','test_image.png','Im pf. Choi. Its public thread.',6),(5,0,0,'2014-06-19 17:42:50','test_image.png','Im pf. Joo. Friends thread.',5),(6,1,0,'2014-06-19 17:43:58','test_image.png','Joo. public thread.',5),(7,1,0,'2014-06-19 17:44:42','test_image.png','Namhoon. public. 한글 나랏말씀이 귕국에 달하시데',1),(8,0,0,'2014-06-19 17:45:38','test_image.png','Namhoon. friends. ^^ Smile every day. ^.^ ^-^ !@#$^&*()_+|',1);",
"ALTER TABLE pine_threads ENABLE KEYS;",
"UNLOCK TABLES;",
"DROP TABLE IF EXISTS pine_threads_likes;",
"SET @saved_cs_client     = @@character_set_client;",
"SET character_set_client = utf8;",
"CREATE TABLE pine_threads_likes ("
"  id int(11) NOT NULL AUTO_INCREMENT,"
"  threads_id int(11) NOT NULL,"
"  users_id int(11) NOT NULL,"
"  PRIMARY KEY (id),"
"  UNIQUE KEY threads_id (threads_id,users_id),"
"  KEY pine_threads_likes_32be03cd (threads_id),"
"  KEY pine_threads_likes_df138c17 (users_id),"
"  CONSTRAINT pine_threads_likes_users_id_31836c347967def5_fk_pine_users_id FOREIGN KEY (users_id) REFERENCES pine_users (id),"
"  CONSTRAINT pine_threads_likes_threads_id_7f7d78b6addeba4_fk_pine_threads_id FOREIGN KEY (threads_id) REFERENCES pine_threads (id)"
") ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;",
"SET character_set_client = @saved_cs_client;",
"LOCK TABLES pine_threads_likes WRITE;",
"ALTER TABLE pine_threads_likes DISABLE KEYS;",
"INSERT INTO pine_threads_likes VALUES (2,8,2),(4,8,3),(1,8,4),(5,8,5),(6,8,6),(3,8,7),(7,8,8);",
"ALTER TABLE pine_threads_likes ENABLE KEYS;",
"UNLOCK TABLES;",
"DROP TABLE IF EXISTS pine_threads_readers;",
"SET @saved_cs_client     = @@character_set_client;",
"SET character_set_client = utf8;",
"CREATE TABLE pine_threads_readers ("
"  id int(11) NOT NULL AUTO_INCREMENT,"
"  threads_id int(11) NOT NULL,"
"  users_id int(11) NOT NULL,"
"  PRIMARY KEY (id),"
"  UNIQUE KEY threads_id (threads_id,users_id),"
"  KEY pine_threads_readers_32be03cd (threads_id),"
"  KEY pine_threads_readers_df138c17 (users_id),"
"  CONSTRAINT pine_threads_readers_users_id_c24b03c0628e83e_fk_pine_users_id FOREIGN KEY (users_id) REFERENCES pine_users (id),"
"  CONSTRAINT pine_threads_reade_threads_id_edba508b22481e1_fk_pine_threads_id FOREIGN KEY (threads_id) REFERENCES pine_threads (id)"
") ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8;",
"SET character_set_client = @saved_cs_client;",
"LOCK TABLES pine_threads_readers WRITE;",
"ALTER TABLE pine_threads_readers DISABLE KEYS;",
"INSERT INTO pine_threads_readers VALUES (7,1,1),(2,1,2),(4,1,3),(1,1,4),(5,1,5),(6,1,6),(3,1,7),(8,1,8),(15,2,1),(10,2,2),(12,2,3),(9,2,4),(13,2,5),(14,2,6),(11,2,7),(16,2,8),(17,3,1),(18,3,5),(19,3,6),(20,4,1),(21,4,5),(22,4,6),(23,5,1),(24,5,5),(25,5,6),(26,6,1),(27,6,5),(28,6,6),(35,7,1),(30,7,2),(32,7,3),(29,7,4),(33,7,5),(34,7,6),(31,7,7),(36,7,8),(43,8,1),(38,8,2),(40,8,3),(37,8,4),(41,8,5),(42,8,6),(39,8,7),(44,8,8);",
"ALTER TABLE pine_threads_readers ENABLE KEYS;",
"UNLOCK TABLES;",
"DROP TABLE IF EXISTS pine_threads_reports;",
"SET @saved_cs_client     = @@character_set_client;",
"SET character_set_client = utf8;",
"CREATE TABLE pine_threads_reports ("
"  id int(11) NOT NULL AUTO_INCREMENT,"
"  threads_id int(11) NOT NULL,"
"  users_id int(11) NOT NULL,"
"  PRIMARY KEY (id),"
"  UNIQUE KEY threads_id (threads_id,users_id),"
"  KEY pine_threads_reports_32be03cd (threads_id),"
"  KEY pine_threads_reports_df138c17 (users_id),"
"  CONSTRAINT pine_threads_reports_users_id_152811a21d6045e8_fk_pine_users_id FOREIGN KEY (users_id) REFERENCES pine_users (id),"
"  CONSTRAINT pine_threads_repo_threads_id_16416340aba1beb9_fk_pine_threads_id FOREIGN KEY (threads_id) REFERENCES pine_threads (id)"
") ENGINE=InnoDB DEFAULT CHARSET=utf8;",
"SET character_set_client = @saved_cs_client;",
"LOCK TABLES pine_threads_reports WRITE;",
"ALTER TABLE pine_threads_reports DISABLE KEYS;",
"ALTER TABLE pine_threads_reports ENABLE KEYS;",
"UNLOCK TABLES;",
"DROP TABLE IF EXISTS pine_users;",
"SET @saved_cs_client     = @@character_set_client;",
"SET character_set_client = utf8;",
"CREATE TABLE pine_users ("
"  id int(11) NOT NULL AUTO_INCREMENT,"
"  device varchar(10) NOT NULL,"
"  push_id varchar(255) DEFAULT NULL,"
"  account_id int(11) NOT NULL,"
"  phone_id int(11) NOT NULL,"
"  PRIMARY KEY (id),"
"  UNIQUE KEY account_id (account_id),"
"  UNIQUE KEY phone_id (phone_id),"
"  CONSTRAINT pine_users_phone_id_976789182fd3bf5_fk_pine_phones_id FOREIGN KEY (phone_id) REFERENCES pine_phones (id),"
"  CONSTRAINT pine_users_account_id_11a5bea588830b65_fk_auth_user_id FOREIGN KEY (account_id) REFERENCES auth_user (id)"
") ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;",
"SET character_set_client = @saved_cs_client;",
"LOCK TABLES pine_users WRITE;",
"ALTER TABLE pine_users DISABLE KEYS;",
"INSERT INTO pine_users VALUES (1,'none','',1,1),(2,'ios','',2,2),(3,'android','APA91bES_sJ4byb5jWI_k5943BglqrV3B-8TsPXxcI2mLrTxUZGjqM89qsPD0hproWWN-CPP0lkKJe5GpTWyORtn9NCRoyFx43WaCbJaraDqukX2CPdWjebSDlEXOzyFE602Aw-bmNNkG8B20c0JFAVjrN2nBrvNSK0xraOU4rSEhlD1ZKOjGRs',3,3),(4,'none','',4,4),(5,'none','',5,5),(6,'none','',6,6),(7,'none','',7,7),(8,'none','',8,8),(9,'none','',9,9),(10,'none','',10,11);",
"ALTER TABLE pine_users ENABLE KEYS;",
"UNLOCK TABLES;",
"DROP TABLE IF EXISTS pine_users_blocks;",
"SET @saved_cs_client     = @@character_set_client;",
"SET character_set_client = utf8;",
"CREATE TABLE pine_users_blocks ("
"  id int(11) NOT NULL AUTO_INCREMENT,"
"  from_users_id int(11) NOT NULL,"
"  to_users_id int(11) NOT NULL,"
"  PRIMARY KEY (id),"
"  UNIQUE KEY from_users_id (from_users_id,to_users_id),"
"  KEY pine_users_blocks_68fb31d2 (from_users_id),"
"  KEY pine_users_blocks_85bdb7d3 (to_users_id),"
"  CONSTRAINT pine_users_blocks_to_users_id_29eb2368f5ff71f2_fk_pine_users_id FOREIGN KEY (to_users_id) REFERENCES pine_users (id),"
"  CONSTRAINT pine_users_block_from_users_id_59a23e75366b4269_fk_pine_users_id FOREIGN KEY (from_users_id) REFERENCES pine_users (id)"
") ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;",
"SET character_set_client = @saved_cs_client;",
"LOCK TABLES pine_users_blocks WRITE;",
"ALTER TABLE pine_users_blocks DISABLE KEYS;",
"INSERT INTO pine_users_blocks VALUES (1,2,6);",
"ALTER TABLE pine_users_blocks ENABLE KEYS;",
"UNLOCK TABLES;",
"DROP TABLE IF EXISTS pine_users_followings;",
"SET @saved_cs_client     = @@character_set_client;",
"SET character_set_client = utf8;",
"CREATE TABLE pine_users_followings ("
"  id int(11) NOT NULL AUTO_INCREMENT,"
"  from_users_id int(11) NOT NULL,"
"  to_users_id int(11) NOT NULL,"
"  PRIMARY KEY (id),"
"  UNIQUE KEY from_users_id (from_users_id,to_users_id),"
"  KEY pine_users_followings_68fb31d2 (from_users_id),"
"  KEY pine_users_followings_85bdb7d3 (to_users_id),"
"  CONSTRAINT pine_users_followi_to_users_id_38dec706e4420637_fk_pine_users_id FOREIGN KEY (to_users_id) REFERENCES pine_users (id),"
"  CONSTRAINT pine_users_follo_from_users_id_32aa1cd5c0dd1bd2_fk_pine_users_id FOREIGN KEY (from_users_id) REFERENCES pine_users (id)"
") ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;",
"SET character_set_client = @saved_cs_client;",
"LOCK TABLES pine_users_followings WRITE;",
"ALTER TABLE pine_users_followings DISABLE KEYS;",
"INSERT INTO pine_users_followings VALUES (1,2,5),(2,3,5),(3,4,5),(4,5,7),(5,5,8),(7,6,2),(8,6,3),(6,6,4);",
"ALTER TABLE pine_users_followings ENABLE KEYS;",
"UNLOCK TABLES;",
"DROP TABLE IF EXISTS pine_users_friend_phones;",
"SET @saved_cs_client     = @@character_set_client;",
"SET character_set_client = utf8;",
"CREATE TABLE pine_users_friend_phones ("
"  id int(11) NOT NULL AUTO_INCREMENT,"
"  users_id int(11) NOT NULL,"
"  phones_id int(11) NOT NULL,"
"  PRIMARY KEY (id),"
"  UNIQUE KEY users_id (users_id,phones_id),"
"  KEY pine_users_friend_phones_df138c17 (users_id),"
"  KEY pine_users_friend_phones_87ddcb00 (phones_id),"
"  CONSTRAINT pine_users_friend_p_phones_id_7725f86b7e63ecc8_fk_pine_phones_id FOREIGN KEY (phones_id) REFERENCES pine_phones (id),"
"  CONSTRAINT pine_users_friend_pho_users_id_41bab964d09cc4ce_fk_pine_users_id FOREIGN KEY (users_id) REFERENCES pine_users (id)"
") ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;",
"SET character_set_client = @saved_cs_client;",
"LOCK TABLES pine_users_friend_phones WRITE;",
"ALTER TABLE pine_users_friend_phones DISABLE KEYS;",
"INSERT INTO pine_users_friend_phones VALUES (2,1,2),(5,1,3),(1,1,4),(6,1,5),(7,1,6),(3,1,7),(8,1,8),(4,1,9),(9,2,1),(13,2,3),(10,2,4),(11,2,5),(12,2,10),(14,3,1),(15,3,2),(16,3,4),(17,3,5),(18,3,10),(19,4,1),(20,4,2),(22,4,3),(21,4,5),(23,5,1),(24,5,7),(25,5,8),(26,6,1),(27,6,2),(30,6,3),(28,6,4),(29,6,5),(31,7,1),(32,10,1),(33,10,2),(35,10,3),(34,10,4);",
"ALTER TABLE pine_users_friend_phones ENABLE KEYS;",
"UNLOCK TABLES;",
"DROP TABLE IF EXISTS pine_users_friends;",
"SET @saved_cs_client     = @@character_set_client;",
"SET character_set_client = utf8;",
"CREATE TABLE pine_users_friends ("
"  id int(11) NOT NULL AUTO_INCREMENT,"
"  from_users_id int(11) NOT NULL,"
"  to_users_id int(11) NOT NULL,"
"  PRIMARY KEY (id),"
"  UNIQUE KEY from_users_id (from_users_id,to_users_id),"
"  KEY pine_users_friends_68fb31d2 (from_users_id),"
"  KEY pine_users_friends_85bdb7d3 (to_users_id),"
"  CONSTRAINT pine_users_friends_to_users_id_597e31c35e90a12f_fk_pine_users_id FOREIGN KEY (to_users_id) REFERENCES pine_users (id),"
"  CONSTRAINT pine_users_frien_from_users_id_48d4f0f01dda132c_fk_pine_users_id FOREIGN KEY (from_users_id) REFERENCES pine_users (id)"
") ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8;",
"SET character_set_client = @saved_cs_client;",
"LOCK TABLES pine_users_friends WRITE;",
"ALTER TABLE pine_users_friends DISABLE KEYS;",
"INSERT INTO pine_users_friends VALUES (21,1,2),(29,1,3),(36,1,4),(41,1,5),(45,1,6),(48,1,7),(50,1,8),(54,1,10),(17,2,1),(30,2,3),(37,2,4),(55,2,10),(25,3,1),(26,3,2),(38,3,4),(56,3,10),(33,4,1),(34,4,2),(35,4,3),(39,5,1),(46,5,6),(43,6,1),(44,6,5),(47,7,1),(49,8,1),(51,10,1),(52,10,2),(53,10,3);",
"ALTER TABLE pine_users_friends ENABLE KEYS;",
"UNLOCK TABLES;",
"SET TIME_ZONE=@OLD_TIME_ZONE;",
"SET SQL_MODE=@OLD_SQL_MODE;",
"SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;",
"SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;",
"SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT;",
"SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS;",
"SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION;",
"SET SQL_NOTES=@OLD_SQL_NOTES;"
]


def generate_func(idx):
    def query_func(index):
        return migrations.RunSQL(sql[index])
    return query_func(idx)


class Migration(migrations.Migration):
    dependencies = [
        ('pine', '0001_initial'),
    ]
    
    operations = [generate_func(i) for i in range(len(sql))]
