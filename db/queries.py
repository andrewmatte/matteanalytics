save_event = "INSERT INTO events (who, document, referrer) VALUES ($1::varchar, $2::varchar, $3::varchar);"

create_signup = "INSERT INTO accounts (email, salt, hashed_salted_password) VALUES ($1, $2, $3) RETURNING *;"

create_session = "INSERT INTO sessions "