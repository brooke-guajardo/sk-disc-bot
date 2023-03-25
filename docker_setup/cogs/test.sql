BEGIN
    IF NOT EXISTS (SELECT * FROM players WHERE player_name = ? )
    BEGIN
        INSERT INTO players (player_id, player_name)
        VALUES ((SELECT COUNT( char_player_id) FROM characters) + 1,?)
    END
END