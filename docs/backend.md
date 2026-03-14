# ER diagram with system descriptions written into db tables

## General instructions

Db is PostgreSQL. Use FastAPI, sqlalchemy and orm. 

The architecture is divided into folders: routes, schemas, models, services, db. 
Each folder contain file for every entity. 

- routes: endpoitns
- services: logic
- schemas: pydantic types
- models: database models and tables, already created, do not change anything here
- db: functions that interact directly with database

Each entity should have CRUD. Each listing should return data like this: 
{
    "items": array of data
    "limit": pagination
    "total": total number of elements in db
    "offset": pagination
}

Each listing should support two params, order (ascending or descending) and order_by, 
each entity can have defined keys that can be used to order_by.

Each error should be catched and returned nice message. 
Message should be only general like: "could not load data" for each get request, it should not be specified by the entity

## Tag System

Group tags into categories. Admin can create and edit tags or tag_categories. 
The tags will be assigned to songs, it will create catologue of songs.

The tags can be retrieved also by categories. Or the categories should also retrieve all tags they have.

Tags can be modified only by admin.

tag
-----------
id (PK)
name (NOT NULL)
tag_category_id (FK -> tag_category.id, NOT NULL)
order_index

tag_category
-----------
id (PK)
name (NOT NULL)
order_index
}

## User System

System with 3 possible roles: admin, editor and common.

Official content can be added by editor. Common user can add unofficial content to songs.
Common user can also create and edit songs and their official content, 
but each request has to be reviewed and accepted by editor.

Each role should have rights of the lower one. 
There should be a seeder with one use of each role.

Admin should have rights to block or delete accounts, as well as grant editor rights to common users. 
Admin can create accounts.

user_role
-----------
id (PK)
role (NOT NULL) 

person
-----------
id (PK)
name (NOT NULL)
surname (NOT NULL)
description (Long rich text string)
avatar (FK -> static_content.id)

user - specialization of person
-----------
id (PK)
person_id (FK -> person.id)
email (UNIQUE, NOT NULL)
mobile (UNIQUE)
role_id (user_role.id, NOT NULL)
registered_at

## Content System

Content_base is unique id for each content that can be edited or created by users, 
e.g. song will have its own id, but also a content_id, so it can be targeted in the review process.

Static content is used for static files. 
They should be stored in some folder, that will be directly on the server, and in the db there should be path to that file.

Song can have score and arrangement. Score is official content, and song can have only one, has to be musescore mscz file.
Song can have any number of arrangements, they can be added by common user without review.

Song arrangements can be retrieved by song_id.

content_base
-----------
id (PK)

static_content
-----------
id (PK)
content_base_id (FK -> content_base.id, NOT NULL)
path (UNIQUE, NOT NULL)

song_score
-----------
id (PK)
content_base_id (FK -> content_base.id, NOT NULL)
song_id (FK -> song.id, NOT NULL)
static_content_id (FK -> static_content.id, NOT NULL)
added_at

song_arrangement
-----------
id (PK)
content_base_id (FK -> content_base.id, NOT NULL)
title
author
description
song_id (FK -> song.id, NOT NULL)
added_by_user_id (FK -> user.id)
added_at
file_type (ENUM - mscz, PDF)
static_content_id (FK -> static_content.id)

song_arrangement_tag
-----------
song_arrangement_id (FK -> song_arrangement.id)
tag_id (FK -> tag.id)
PRIMARY KEY (song_arrangement_id, tag_id)


## Song system

Song can have many tags, many authors, one official only mscz score, many arrangements and many related songs. 
For text, each song can have many song parts, each as rich content.
Each song can be assigned to many celebrations.

Song should be easily filtered by tags, full text search and can be ordered.
When filtered by tags, if multiple tags are provided apply two rules:
- between tags of same category is logical OR
- between tag categories, there is logical AND

When someone create song, it can create also song_score, song arrangements, song authors, song_parts, and link it to some other related songs and add tags to it.

author - not registered user, used to list songs for authors
-----------
id (PK)
content_base_id (FK -> content_base.id, NOT NULL)
person_id (FK -> person.id, NOT NULL)
added_by_user (FK -> user.id)
added_at

song_author
-----------
song_id (FK -> song.id)
author_id (FK -> author.id)
PRIMARY KEY (song.id, author.id)

song
-----------
id (PK)
content_base_id (FK -> content_base.id)
title (NOT NULL, unique)
description (Long rich text)
added_by_user (FK -> user.id)
added_at
last_edited_at

related_song - song that might be marked as similar to some other song.
-----------
song_id (FK -> song.id)
song_id (FK -> song.id)
PRIMARY_KEY (song_id, song_id)

song_tag
-----------
song_id (FK -> song.id)
tag_id (FK -> tag.id)
PRIMARY KEY (song_id, tag_id)

song_part
-----------
id (PK)
song_id (FK -> song.id)
text (long rich content)
title (automatically derived from first line of text)
order_index


## Reviewing system

If common user wants to edit or create new song, he has to create a request that has to be approved by editor. 
Common user can still add song arrangements without edit request or approval.  

The request will create a new content_base entity, that can be used to update the new entity. 
For now it will be songs, but this way, it can be expanded to other content types.

review_request
-----------
id (PK)
description
requester_id (FK -> user.id, NOT NULL)
editor_id (FK -> user.id)
new_entity (FK -> content_base.id, NOT NULL)
original_id (FK -> content_base.id)
created_at
closed_at

review_comment
-----------
id (PK)
review_request_id (FK -> review_request.id)
content
created_by_user_id (FK -> user.id, NOT NULL)
created_at

## Calendar system

Celebrations can be grouped into categories.
Each celebration can have many songs with additional data. Each song can be bound to some celebration(mass) part and liturgic cycle.

Celebrations, celebration_categories, celebration_parts should be modified only by admin.

Celebration songs can be created by editor too.

celebration_category
-----------
id (PK)
name
order_index

celebration
-----------
id (PK) 
celebration_category_id (FK → celebration_category.id)
name
description
day
month
created_at

celebration_part (mass parts)
-----------
id (PK)
name
order_index

celebration_song
-----------
id (PK)
celebration_id (FK -> celebration.id)
song_id (FK -> songs.id)
celebration_part_id (FK -> celebration_part.id)
song_part_number
song_part_name
is_prescribed (boolean)
liturgical_cycle  (ENUM A,B,C,NULL)
order_index
description

