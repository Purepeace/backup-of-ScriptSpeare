-- MySQL Script generated by MySQL Workbench
-- Sat 02 Feb 2019 14:59:57 GMT
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema ScriptspeareDB
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema ScriptspeareDB
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `ScriptspeareDB` ;
USE `ScriptspeareDB` ;

-- -----------------------------------------------------
-- Table `ScriptspeareDB`.`Genres`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ScriptspeareDB`.`Genres` (
  `genre_id` TINYINT NOT NULL,
  `genre` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`genre_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ScriptspeareDB`.`Plays`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ScriptspeareDB`.`Plays` (
  `play_id` SMALLINT NOT NULL,
  `title` TEXT NOT NULL,
  `genre_id_fk` TINYINT NOT NULL,
  PRIMARY KEY (`play_id`),
  INDEX `fk_Plays_Genres_idx` (`genre_id_fk` ASC) VISIBLE,
  CONSTRAINT `fk_Plays_Genres`
    FOREIGN KEY (`genre_id_fk`)
    REFERENCES `ScriptspeareDB`.`Genres` (`genre_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ScriptspeareDB`.`Adaptations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ScriptspeareDB`.`Adaptations` (
  `adaptation_id` SMALLINT NOT NULL,
  `play_id_fk` SMALLINT NOT NULL,
  `year` SMALLINT NOT NULL,
  `lead_actor` VARCHAR(255) NOT NULL,
  `s3_video_link` TEXT NOT NULL,
  `s3_xml_link` TEXT NOT NULL,
  PRIMARY KEY (`adaptation_id`, `play_id_fk`),
  INDEX `fk_adaptation_id_Plays1_idx` (`play_id_fk` ASC) VISIBLE,
  CONSTRAINT `fk_adaptation_id_Plays1`
    FOREIGN KEY (`play_id_fk`)
    REFERENCES `ScriptspeareDB`.`Plays` (`play_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ScriptspeareDB`.`Annotation_types`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ScriptspeareDB`.`Annotation_types` (
  `annotation_type_id` TINYINT NOT NULL,
  `annotation_type` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`annotation_type_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ScriptspeareDB`.`Global_annotations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ScriptspeareDB`.`Global_annotations` (
  `annotation_id` MEDIUMINT NOT NULL,
  `play_id_fk` SMALLINT NOT NULL,
  `line_number` MEDIUMINT NOT NULL,
  `annotation_type_id_fk` TINYINT NOT NULL,
  `annotation` MEDIUMTEXT NOT NULL,
  PRIMARY KEY (`annotation_id`),
  INDEX `fk_Global_Annotations_Plays1_idx` (`play_id_fk` ASC) VISIBLE,
  INDEX `fk_Global_annotations_Annotation_types1_idx` (`annotation_type_id_fk` ASC) VISIBLE,
  CONSTRAINT `fk_Global_Annotations_Plays1`
    FOREIGN KEY (`play_id_fk`)
    REFERENCES `ScriptspeareDB`.`Plays` (`play_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Global_annotations_Annotation_types1`
    FOREIGN KEY (`annotation_type_id_fk`)
    REFERENCES `ScriptspeareDB`.`Annotation_types` (`annotation_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ScriptspeareDB`.`Adaptation_annotations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ScriptspeareDB`.`Adaptation_annotations` (
  `annotation_id` MEDIUMINT NOT NULL,
  `adaptation_id_fk` SMALLINT NOT NULL,
  `play_id_fk` SMALLINT NOT NULL,
  `line_number` MEDIUMINT NOT NULL,
  `annotation_type_id_fk` TINYINT NOT NULL,
  `annotation` MEDIUMTEXT NOT NULL,
  PRIMARY KEY (`annotation_id`),
  INDEX `fk_Adaptation_annotations_Adaptations1_idx` (`adaptation_id_fk` ASC, `play_id_fk` ASC) VISIBLE,
  INDEX `fk_Adaptation_annotations_Annotation_types1_idx` (`annotation_type_id_fk` ASC) VISIBLE,
  CONSTRAINT `fk_Adaptation_annotations_Adaptations1`
    FOREIGN KEY (`adaptation_id_fk` , `play_id_fk`)
    REFERENCES `ScriptspeareDB`.`Adaptations` (`adaptation_id` , `play_id_fk`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Adaptation_annotations_Annotation_types1`
    FOREIGN KEY (`annotation_type_id_fk`)
    REFERENCES `ScriptspeareDB`.`Annotation_types` (`annotation_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
