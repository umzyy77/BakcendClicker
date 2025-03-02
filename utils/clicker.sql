SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS buy;
DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS enemy;
DROP TABLE IF EXISTS enhancement;
DROP TABLE IF EXISTS type_enhancement;
SET FOREIGN_KEY_CHECKS = 1;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";
SET NAMES utf8mb4;

-- 🔹 Table `type_enhancement`
CREATE TABLE `type_enhancement` (
  `id_type` INT NOT NULL AUTO_INCREMENT,
  `name_type` VARCHAR(5) NOT NULL,
  PRIMARY KEY (`id_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 🔹 Table `enhancement`
CREATE TABLE `enhancement` (
  `id_enhancement` INT NOT NULL AUTO_INCREMENT,
  `experience_cost` INT NOT NULL,
  `boost_value` INT NOT NULL,
  `id_type` INT NOT NULL,
  PRIMARY KEY (`id_enhancement`),
  CONSTRAINT fk_enhancement_type FOREIGN KEY (`id_type`) REFERENCES `type_enhancement`(`id_type`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 🔹 Table `enemy`
CREATE TABLE `enemy` (
  `level` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  `total_life` INT NOT NULL,
  PRIMARY KEY (`level`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 🔹 Table `player`
CREATE TABLE `player` (
  `id_player` INT NOT NULL AUTO_INCREMENT,
  `pseudo` VARCHAR(50) NOT NULL,
  `total_experience` INT NOT NULL,
  `id_enemy` INT NOT NULL,
  PRIMARY KEY (`id_player`),
  CONSTRAINT fk_player_enemy FOREIGN KEY (`id_enemy`) REFERENCES `enemy`(`level`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 🔹 Table `buy`
CREATE TABLE `buy` (
  `id_player` INT NOT NULL,
  `id_enhancement` INT NOT NULL,
  PRIMARY KEY (`id_player`, `id_enhancement`),
  CONSTRAINT fk_buy_player FOREIGN KEY (`id_player`) REFERENCES `player`(`id_player`) ON DELETE CASCADE,
  CONSTRAINT fk_buy_enhancement FOREIGN KEY (`id_enhancement`) REFERENCES `enhancement`(`id_enhancement`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ✅ Insertion des données

-- 🟢 type_enhancement
INSERT INTO `type_enhancement` (`name_type`) VALUES
('dps'),
('exp');

-- 🟢 enhancement
INSERT INTO `enhancement` (`experience_cost`, `boost_value`, `id_type`) VALUES
(0, 1, 1),
(50, 2, 1),
(0, 1, 2),
(50, 2, 2);

-- 🟢 enemy
INSERT INTO `enemy` (`name`, `total_life`) VALUES
('blue slime', 10),
('green slime', 20),
('red slime', 30),
('yellow slime', 40),
('king slime', 50);

-- 🟢 player
INSERT INTO `player` (`pseudo`, `total_experience`, `id_enemy`) VALUES
('OmegaZell', 0, 1),
('Sparadrap', 0, 1);

-- 🟢 buy
INSERT INTO `buy` (`id_player`, `id_enhancement`) VALUES
(1, 1),
(2, 1);

COMMIT;
