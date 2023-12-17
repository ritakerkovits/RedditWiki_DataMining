SELECT 
ug_user
,ug_group
,ug_expiry
FROM 
dbo.user_groups as ug_db
WHERE
ug_db.ug_group = 'bot'