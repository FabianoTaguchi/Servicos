CREATE DATABASE IF NOT EXISTS `agromail` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `agromail`;

CREATE TABLE IF NOT EXISTS `user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(80) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_user_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `cultivares` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(120) NOT NULL,
  `especie` VARCHAR(120),
  `descricao` TEXT,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_cultivares_nome` (`nome`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `ordens` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `titulo` VARCHAR(200) NOT NULL,
  `descricao` TEXT,
  `status` VARCHAR(20) DEFAULT 'aberta',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `solicitante_id` INT NOT NULL,
  `cultivar_id` INT,
  PRIMARY KEY (`id`),
  KEY `ix_ordens_status` (`status`),
  KEY `ix_ordens_solicitante` (`solicitante_id`),
  CONSTRAINT `fk_ordens_user` FOREIGN KEY (`solicitante_id`) REFERENCES `user` (`id`),
  CONSTRAINT `fk_ordens_cultivar` FOREIGN KEY (`cultivar_id`) REFERENCES `cultivares` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;