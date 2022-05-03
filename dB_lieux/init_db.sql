DROP TABLE IF EXISTS pays, ville; 
SET GLOBAL local_infile=1;
CREATE TABLE `pays`(
	`lang` VARCHAR(5),
	`libelle_lang` VARCHAR(50),
	`pays_code_alpha2` CHAR(2),
	`pays_code_alpha3` CHAR(3),
	`pays_code_numeric` CHAR(3),
	`libelle` VARCHAR(200)  
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

LOAD DATA LOCAL
INFILE 'E:\\NAM-IP\\catTools-git\\dB_lieux\\pays.csv' INTO TABLE `pays`
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n' IGNORE 1 LINES;

CREATE TABLE ville(
	id INT PRIMARY KEY auto_increment,
    code_pays CHAR(2) NOT NULL,
    libelle VARCHAR(300) NOT NULL    
    );
    
LOAD DATA LOCAL
INFILE 'E:\\NAM-IP\\catTools-git\\dB_lieux\\cities_merge.csv' 
INTO TABLE ville
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n' IGNORE 1 LINES
(code_pays, libelle)
SET ID = NULL;

CREATE INDEX libelle_ville ON ville(libelle);

