DELETE
FROM crackerjacksapi_team
WHERE crackerjacksapi_team.id IS NOT NULL

UPDATE crackerjacksapi_crackerjacksuser
SET profile_image_url = 'https://i.imgur.com/1AvDPdP.jpg'
WHERE user_id = 3;

DELETE
FROM crackerjacksapi_follower