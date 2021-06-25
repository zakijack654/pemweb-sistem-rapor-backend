-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 19, 2021 at 03:55 PM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 8.0.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sistem_rapor_pweb`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `check_nilai` (IN `nilai` DECIMAL(5,2))  BEGIN
	IF (nilai > 100) OR (nilai < 0) THEN
    	SIGNAL SQLSTATE '45000'
        	SET MESSAGE_TEXT = 'Nilai yang dimasukkan tidak valid!';
    END IF;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id_admin` tinyint(3) UNSIGNED NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `reg_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `guru`
--

CREATE TABLE `guru` (
  `id_guru` tinyint(3) UNSIGNED NOT NULL,
  `nama_guru` varchar(50) NOT NULL,
  `nip` varchar(50) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  `isWaliKelas` tinyint(1) NOT NULL,
  `isActive` tinyint(1) NOT NULL DEFAULT 1,
  `reg_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `jurusan`
--

CREATE TABLE `jurusan` (
  `id_jurusan` tinyint(3) UNSIGNED NOT NULL,
  `nama_jurusan` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `kelas`
--

CREATE TABLE `kelas` (
  `id_kelas` tinyint(3) UNSIGNED NOT NULL,
  `jenjang_kelas` varchar(3) NOT NULL,
  `urutan_kelas` enum('A','B','C','D') NOT NULL,
  `jurusan` tinyint(3) UNSIGNED NOT NULL,
  `wali_kelas` tinyint(3) UNSIGNED NOT NULL,
  `reg_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `mapel`
--

CREATE TABLE `mapel` (
  `id_mapel` tinyint(3) UNSIGNED NOT NULL,
  `nama_mapel` varchar(50) NOT NULL,
  `jurusan` tinyint(3) UNSIGNED NOT NULL,
  `reg_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `periode_ajaran`
--

CREATE TABLE `periode_ajaran` (
  `id` smallint(5) UNSIGNED NOT NULL,
  `tahun_ajaran` varchar(9) NOT NULL,
  `semester` enum('Ganjil','Genap') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `rapor_nilai`
--

CREATE TABLE `rapor_nilai` (
  `id` mediumint(8) UNSIGNED NOT NULL,
  `nis` varchar(10) NOT NULL,
  `id_mapel` tinyint(3) UNSIGNED NOT NULL,
  `nilai` decimal(5,2) UNSIGNED DEFAULT NULL,
  `periode_nilai` smallint(5) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Triggers `rapor_nilai`
--
DELIMITER $$
CREATE TRIGGER `nilai_before_insert` BEFORE INSERT ON `rapor_nilai` FOR EACH ROW BEGIN
	CALL check_nilai(new.nilai);
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `nilai_before_update` BEFORE UPDATE ON `rapor_nilai` FOR EACH ROW BEGIN
	CALL check_nilai(new.nilai);
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `siswa`
--

CREATE TABLE `siswa` (
  `nis` varchar(10) NOT NULL,
  `nama_siswa` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `jenkel` set('L','P') NOT NULL,
  `kelas` tinyint(3) UNSIGNED NOT NULL,
  `isActive` tinyint(1) NOT NULL DEFAULT 1,
  `reg_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id_admin`);

--
-- Indexes for table `guru`
--
ALTER TABLE `guru`
  ADD PRIMARY KEY (`id_guru`),
  ADD UNIQUE KEY `nip` (`nip`);

--
-- Indexes for table `jurusan`
--
ALTER TABLE `jurusan`
  ADD PRIMARY KEY (`id_jurusan`);

--
-- Indexes for table `kelas`
--
ALTER TABLE `kelas`
  ADD PRIMARY KEY (`id_kelas`),
  ADD KEY `jurusan_kelas` (`jurusan`),
  ADD KEY `wali_kelas` (`wali_kelas`);

--
-- Indexes for table `mapel`
--
ALTER TABLE `mapel`
  ADD PRIMARY KEY (`id_mapel`),
  ADD KEY `jurusan_mapel` (`jurusan`);

--
-- Indexes for table `periode_ajaran`
--
ALTER TABLE `periode_ajaran`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tahun_ajaran` (`tahun_ajaran`);

--
-- Indexes for table `rapor_nilai`
--
ALTER TABLE `rapor_nilai`
  ADD PRIMARY KEY (`id`),
  ADD KEY `nis_rapor` (`nis`),
  ADD KEY `mapel_rapor` (`id_mapel`),
  ADD KEY `periode_nilai` (`periode_nilai`);

--
-- Indexes for table `siswa`
--
ALTER TABLE `siswa`
  ADD PRIMARY KEY (`nis`),
  ADD KEY `kelas_siswa` (`kelas`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id_admin` tinyint(3) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `guru`
--
ALTER TABLE `guru`
  MODIFY `id_guru` tinyint(3) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `jurusan`
--
ALTER TABLE `jurusan`
  MODIFY `id_jurusan` tinyint(3) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `kelas`
--
ALTER TABLE `kelas`
  MODIFY `id_kelas` tinyint(3) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `mapel`
--
ALTER TABLE `mapel`
  MODIFY `id_mapel` tinyint(3) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `periode_ajaran`
--
ALTER TABLE `periode_ajaran`
  MODIFY `id` smallint(5) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `rapor_nilai`
--
ALTER TABLE `rapor_nilai`
  MODIFY `id` mediumint(8) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `kelas`
--
ALTER TABLE `kelas`
  ADD CONSTRAINT `jurusan_kelas` FOREIGN KEY (`jurusan`) REFERENCES `jurusan` (`id_jurusan`),
  ADD CONSTRAINT `wali_kelas` FOREIGN KEY (`wali_kelas`) REFERENCES `guru` (`id_guru`);

--
-- Constraints for table `mapel`
--
ALTER TABLE `mapel`
  ADD CONSTRAINT `jurusan_mapel` FOREIGN KEY (`jurusan`) REFERENCES `jurusan` (`id_jurusan`);

--
-- Constraints for table `rapor_nilai`
--
ALTER TABLE `rapor_nilai`
  ADD CONSTRAINT `mapel_rapor` FOREIGN KEY (`id_mapel`) REFERENCES `mapel` (`id_mapel`),
  ADD CONSTRAINT `nis_rapor` FOREIGN KEY (`nis`) REFERENCES `siswa` (`nis`),
  ADD CONSTRAINT `periode_nilai` FOREIGN KEY (`periode_nilai`) REFERENCES `periode_ajaran` (`id`);

--
-- Constraints for table `siswa`
--
ALTER TABLE `siswa`
  ADD CONSTRAINT `kelas_siswa` FOREIGN KEY (`kelas`) REFERENCES `kelas` (`id_kelas`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
