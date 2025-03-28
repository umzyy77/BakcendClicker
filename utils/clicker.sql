SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS player_mission;
DROP TABLE IF EXISTS player_upgrade;
DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS mission;
DROP TABLE IF EXISTS upgrade;
DROP TABLE IF EXISTS difficulty;
DROP TABLE IF EXISTS status;
DROP TABLE IF EXISTS upgrade_level;
SET FOREIGN_KEY_CHECKS = 1;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";
SET NAMES utf8mb4;

-- 🔹 Table `difficulty` (Niveaux de difficulté des missions, avec clics requis)
CREATE TABLE `difficulty` (
  `id_difficulty` INT NOT NULL AUTO_INCREMENT,
  `label` VARCHAR(50) NOT NULL,
  `clicks_required` INT NOT NULL, -- Nombre de clics requis pour accomplir une mission de ce niveau
  PRIMARY KEY (`id_difficulty`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 🔹 Table `status` (Statuts des missions du joueur)
CREATE TABLE `status` (
  `id_status` INT NOT NULL AUTO_INCREMENT,
  `label` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 🔹 Table `player` (Stocke les joueurs)
CREATE TABLE `player` (
  `id_player` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL,
  `hacking_power` INT NOT NULL DEFAULT 1,
  `money` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id_player`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 🔹 Table `upgrade` (Liste des améliorations principales)
CREATE TABLE `upgrade` (
  `id_upgrade` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id_upgrade`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 🔹 Table `upgrade_level` (Niveaux des améliorations)
CREATE TABLE `upgrade_level` (
  `id_level` INT NOT NULL AUTO_INCREMENT,
  `id_upgrade` INT NOT NULL,
  `level` INT NOT NULL,
  `cost` INT NOT NULL,
  `boost_value` INT NOT NULL,
  PRIMARY KEY (`id_level`),
  CONSTRAINT fk_upgrade_level_upgrade FOREIGN KEY (`id_upgrade`) REFERENCES `upgrade`(`id_upgrade`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 🔹 Table `player_upgrade` (Joueur → Améliorations achetées)
CREATE TABLE `player_upgrade` (
  `id_player` INT NOT NULL,
  `id_level` INT NOT NULL,
  PRIMARY KEY (`id_player`, `id_level`),
  CONSTRAINT fk_player_upgrade_player FOREIGN KEY (`id_player`) REFERENCES `player`(`id_player`) ON DELETE CASCADE,
  CONSTRAINT fk_player_upgrade_level FOREIGN KEY (`id_level`) REFERENCES `upgrade_level`(`id_level`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 🔹 Table `mission` (Missions de piratage)
CREATE TABLE `mission` (
  `id_mission` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `id_difficulty` INT NOT NULL,
  `reward_money` INT NOT NULL,
  `reward_power` INT NOT NULL,
  PRIMARY KEY (`id_mission`),
  CONSTRAINT fk_mission_difficulty FOREIGN KEY (`id_difficulty`) REFERENCES `difficulty`(`id_difficulty`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 🔹 Table `player_mission` (Joueur → Missions accomplies avec statut et progression des clics)
CREATE TABLE `player_mission` (
  `id_player` INT NOT NULL,
  `id_mission` INT NOT NULL,
  `id_status` INT NOT NULL,
  `clicks_done` INT NOT NULL DEFAULT 0, -- Suivi des clics réalisés
  PRIMARY KEY (`id_player`, `id_mission`),
  CONSTRAINT fk_player_mission_player FOREIGN KEY (`id_player`) REFERENCES `player`(`id_player`) ON DELETE CASCADE,
  CONSTRAINT fk_player_mission_mission FOREIGN KEY (`id_mission`) REFERENCES `mission`(`id_mission`) ON DELETE CASCADE,
  CONSTRAINT fk_player_mission_status FOREIGN KEY (`id_status`) REFERENCES `status`(`id_status`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE player_progress (
    id_player INT NOT NULL PRIMARY KEY,
    last_unlocked_mission INT NULL,
    FOREIGN KEY (id_player) REFERENCES player(id_player) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- ✅ Insertion des données de base

-- 🟢 Difficulté des missions avec clics requis
INSERT INTO `difficulty` (`label`, `clicks_required`) VALUES ('Facile', 50), ('Moyen', 300), ('Difficile', 1000);

-- 🟢 Statuts des missions
INSERT INTO `status` (`label`) VALUES ('locked'), ('unlocked'), ('in_progress'), ('completed');

-- 🟢 Améliorations disponibles
INSERT INTO `upgrade` (`name`) VALUES ('Processeur Amélioré'), ('Botnet Basique'), ('VPN Sécurisé');

-- 🟢 Niveaux des améliorations
INSERT INTO `upgrade_level` (`id_upgrade`, `level`, `cost`, `boost_value`) VALUES
(1, 1, 100, 2), (1, 2, 300, 5), (1, 3, 700, 10),
(2, 1, 500, 5), (2, 2, 1000, 10), (2, 3, 2000, 20),
(3, 1, 250, 3), (3, 2, 600, 8), (3, 3, 1200, 15);

-- 🟢 Missions disponibles
INSERT INTO `mission` (`name`, `id_difficulty`, `reward_money`, `reward_power`) VALUES
('Pirater un serveur basique', 1, 200, 2),
('Accéder à une banque', 2, 1000, 5),
('Infiltrer un gouvernement', 3, 5000, 10);

-- 🟢 Création de joueurs
INSERT INTO `player` (`username`, `hacking_power`, `money`) VALUES ('NeoHacker', 1, 0), ('DarkShadow', 2, 500);

-- 🟢 Assignation de missions aux joueurs
INSERT INTO `player_mission` (`id_player`, `id_mission`, `id_status`, `clicks_done`) VALUES (1, 1, 3, 10), (1, 2, 2, 50), (2, 3, 4, 300);

-- 🟢 Achats d'améliorations par les joueurs
INSERT INTO `player_upgrade` (`id_player`, `id_level`) VALUES (1, 1), (1, 2), (2, 3);

COMMIT;
