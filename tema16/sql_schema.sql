-- Table to store actor information
CREATE TABLE actors (
    act_id int NOT NULL, -- Unique ID for each actor (Primary Key)
    act_first_name VARCHAR(255), -- Actor's first name
    act_last_name VARCHAR(255),  -- Actor's last name
    act_gender VARCHAR(1), -- Actor's gender (M/F/O - typically one character)
    PRIMARY KEY ("act_id") -- Define 'act_id' as the Primary Key (unique identifier)
); 

-- Table to store movie information
CREATE TABLE movie (
    mov_id int NOT NULL, -- Unique ID for each movie (Primary Key)
    mov_title VARCHAR(255), -- Movie title (name of the movie)
    PRIMARY KEY ("mov_id") -- Define 'mov_id' as the Primary Key (unique identifier)
); 

-- Table to store director information
CREATE TABLE director (
    dir_id int NOT NULL, -- Unique ID for each director (Primary Key)
    dir_first_name VARCHAR(255), -- Director's first name
    dir_last_name VARCHAR(255),  -- Director's last name
    PRIMARY KEY ("dir_id") -- Define 'dir_id' as the Primary Key (unique identifier)
); 

-- Table to store cast information (relationship between movies and actors)
CREATE TABLE movie_cast (
    act_id int, -- Reference to the 'actors' table (actor's ID)
    mov_id int, -- Reference to the 'movie' table (movie's ID)
    role VARCHAR(255), -- Role played by the actor in the movie
    FOREIGN KEY (act_id) REFERENCES actors(act_id) ON DELETE CASCADE, 
    -- Foreign Key linking to 'actors' table, 
    -- 'ON DELETE CASCADE' ensures if an actor is deleted, all related rows in 'movie_cast' are also deleted.
	
    FOREIGN KEY (mov_id) REFERENCES movie(mov_id) ON DELETE CASCADE
    -- Foreign Key linking to 'movie' table,
    -- 'ON DELETE CASCADE' ensures if a movie is deleted, all related rows in 'movie_cast' are also deleted.
); 

-- Table to store information about Oscar awards given to movies
CREATE TABLE oscar_awarded (
    award_id int, -- Unique ID for each Oscar (Primary Key)
    mov_id int, -- Reference to the 'movie' table (movie's ID)
    PRIMARY KEY ("award_id"), -- Define 'award_id' as the Primary Key (unique identifier)
    FOREIGN KEY (mov_id) REFERENCES movie(mov_id) ON DELETE SET NULL
    -- Foreign Key linking to 'movie' table,
    -- 'ON DELETE SET NULL' ensures if a movie is deleted, the 'mov_id' in this table is set to NULL instead of deleting the award.
); 

-- Table to store information about movie direction (relationship between movies and directors)
CREATE TABLE movie_direction (
    dir_id int, -- Reference to the 'director' table (director's ID)
    mov_id int, -- Reference to the 'movie' table (movie's ID)
    FOREIGN KEY (dir_id) REFERENCES director(dir_id) ON DELETE CASCADE,
    -- Foreign Key linking to 'director' table,
    -- 'ON DELETE CASCADE' ensures if a director is deleted, all related rows in 'movie_direction' are also deleted.

    FOREIGN KEY (mov_id) REFERENCES movie(mov_id) ON DELETE CASCADE
    -- Foreign Key linking to 'movie' table,
    -- 'ON DELETE CASCADE' ensures if a movie is deleted, all related rows in 'movie_direction' are also deleted.
); 
