BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "skills" (
	"skills_player_id"	INTEGER NOT NULL UNIQUE,
	"athletics"	INTEGER NOT NULL DEFAULT 0,
	"biology"	INTEGER NOT NULL DEFAULT 0,
	"computers"	INTEGER NOT NULL DEFAULT 0,
	"empathy"	INTEGER NOT NULL DEFAULT 0,
	"engineering"	INTEGER NOT NULL DEFAULT 0,
	"explosives"	INTEGER NOT NULL DEFAULT 0,
	"firearms"	INTEGER NOT NULL DEFAULT 0,
	"investigation"	INTEGER NOT NULL DEFAULT 0,
	"law"	INTEGER NOT NULL DEFAULT 0,
	"lying"	INTEGER NOT NULL DEFAULT 0,
	"melee"	INTEGER NOT NULL DEFAULT 0,
	"perform"	INTEGER NOT NULL DEFAULT 0,
	"piloting"	INTEGER NOT NULL DEFAULT 0,
	"persuasion"	INTEGER NOT NULL DEFAULT 0,
	"sneaking"	INTEGER NOT NULL DEFAULT 0,
	"spacewise"	INTEGER NOT NULL DEFAULT 0,
	"survival"	INTEGER NOT NULL DEFAULT 0,
	"telekinesis"	INTEGER NOT NULL DEFAULT 0,
	"telepathy"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("skills_player_id")
);
CREATE TABLE IF NOT EXISTS "players" (
	"player_id"	INTEGER NOT NULL UNIQUE,
	"player_name"	TEXT NOT NULL UNIQUE,
	"player_deck"	TEXT,
	"player_discord"	NUMERIC UNIQUE,
	"player_char_desc"	TEXT,
	"player_drive"	INTEGER DEFAULT 0,
	"player_hero_points"	INTEGER DEFAULT 0,
	"player_brawn"	INTEGER NOT NULL DEFAULT 1,
	"player_intelligence"	INTEGER NOT NULL DEFAULT 1,
	"player_charm"	INTEGER NOT NULL DEFAULT 1,
	"player_agility"	INTEGER NOT NULL DEFAULT 1,
	"player_wit"	INTEGER NOT NULL DEFAULT 1,
	"player_presence"	INTEGER NOT NULL DEFAULT 1,
	"player_dodge"	INTEGER NOT NULL DEFAULT 0,
	"player_init"	INTEGER NOT NULL DEFAULT 0,
	"player_health"	INTEGER NOT NULL DEFAULT 1,
	"player_current_health"	INTEGER NOT NULL DEFAULT 1,
	"player_dm"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("player_id")
);
CREATE TRIGGER skills_new_player_skills AFTER INSERT ON players
	BEGIN
		INSERT INTO skills (skills_player_id) VALUES ((select player_id from players order by player_id DESC limit 1));
	END;
CREATE TRIGGER player_init_trigger2 UPDATE OF player_presence,player_agility ON players
	BEGIN
		UPDATE players set player_dodge=player_presence + player_agility;
	END;
CREATE TRIGGER player_dodoge_trigger2 UPDATE OF player_wit,player_agility ON players
	BEGIN
		UPDATE players set player_dodge=player_wit + player_agility - 2;
	END;
CREATE TRIGGER player_drive_trigger2 UPDATE OF player_wit,player_presence ON players
	BEGIN
		UPDATE players set player_dodge=player_wit + player_presence;
	END;
CREATE TRIGGER player_drive_trigger AFTER INSERT ON players
	BEGIN
		UPDATE players set player_dodge=player_wit + player_presence;
	END;
CREATE TRIGGER player_dodge_trigger AFTER INSERT ON players
	BEGIN
		UPDATE players set player_dodge=player_wit + player_agility - 2;
	END;
CREATE TRIGGER player_init_trigger AFTER INSERT ON players
	BEGIN
		UPDATE players set player_init=player_agility+player_presence;
	END;
CREATE TRIGGER player_health AFTER UPDATE OF player_brawn ON players
	BEGIN
		UPDATE players set player_health=player_brawn*3;
	END;
CREATE TRIGGER dm_flag AFTER INSERT ON players WHEN
(SELECT COUNT(*) FROM players WHERE player_dm=1) = 0
BEGIN
	UPDATE players SET player_dm=1;
END;
CREATE VIEW character_sheet (
	character_name,
	brawn,
	intelligence,
	charm,
	agility,
	wit,
	presence,
	athletics,
	biology,
	computers,
	empathy,
	engineering,
	explosives,
	firearms,
	investigation,
	law,
	lying,
	melee,
	perform,
	piloting,
	persuasion,
	sneaking,
	spacewise,
	survival,
	telekinesis,
	telepathy)
	
	AS SELECT 
	players.player_name AS character_name,
	players.player_brawn AS brawn,
	players.player_intelligence AS intelligence,
	players.player_charm AS charm,
	players.player_agility AS agility,
	players.player_wit AS wit,
	players.player_presence AS presence,
	athletics,
    biology,
    computers,
    empathy,
    engineering,
    explosives,
    firearms,
    investigation,
    law,
    lying,
    melee,
    perform,
    piloting,
    persuasion,
    sneaking,
    spacewise,
    survival,
    telekinesis,
    telepathy
    FROM skills 
    INNER JOIN players 
    ON skills.skills_player_id=players.player_id;
COMMIT;