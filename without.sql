-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 31, 2022 at 03:08 PM
-- Server version: 10.4.20-MariaDB
-- PHP Version: 7.4.22

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `without`
--

-- --------------------------------------------------------

--
-- Table structure for table `bookingbed`
--

CREATE TABLE `bookingbed` (
  `id` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `bedtype` varchar(50) NOT NULL,
  `HosCode` varchar(100) NOT NULL,
  `medicalhistory` varchar(10) NOT NULL,
  `pname` varchar(100) NOT NULL,
  `pphone` varchar(12) NOT NULL,
  `paddress` varchar(100) NOT NULL,
  `page` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `bookingbed`
--

INSERT INTO `bookingbed` (`id`, `email`, `bedtype`, `HosCode`, `medicalhistory`, `pname`, `pphone`, `paddress`, `page`) VALUES
(1, 'an@gmail.com', 'NormalBed', 'H101', 'No', 'anish', '7896541230', 'hotgi', 20),
(2, 'chetantalla65@gmail.com', 'IcuBed', 'H101', 'Yes', 'Chetan Talla', '7387548974', 'Solapur', 21),
(4, 'anishnr8787@gmail.com', 'IcuBed', 'H101', 'No', 'anish', '7896541230', 'Solapur', 20),
(6, '12@gmail.com', 'VentBed', 'H101', 'No', 'xyz', '7896541230', 'Solapur', 20),
(8, '123@gmail.com', 'VentBed', 'H101', 'No', 'xyz', '7896541230', 'Solapur', 20);

-- --------------------------------------------------------

--
-- Table structure for table `hospitaldata`
--

CREATE TABLE `hospitaldata` (
  `id` int(11) NOT NULL,
  `HosCode` varchar(100) NOT NULL,
  `HosName` varchar(200) NOT NULL,
  `normalbed` int(11) NOT NULL,
  `icubed` int(11) NOT NULL,
  `ventbed` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `hospitaldata`
--

INSERT INTO `hospitaldata` (`id`, `HosCode`, `HosName`, `normalbed`, `icubed`, `ventbed`) VALUES
(1, 'H101 ', 'hospital1', 50, 30, 15),
(2, 'H102 ', 'hospital2', 35, 12, 15);

--
-- Triggers `hospitaldata`
--
DELIMITER $$
CREATE TRIGGER `Delete` BEFORE DELETE ON `hospitaldata` FOR EACH ROW INSERT INTO triger VALUES(null,OLD.HosCode,OLD.normalbed,OLD.icubed,OLD.ventbed,'DELETED',NOW())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `Insert` AFTER INSERT ON `hospitaldata` FOR EACH ROW INSERT INTO triger
VALUES(null,NEW.HosCode,NEW.normalbed,NEW.icubed,NEW.ventbed,'INSERTED',NOW())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `Update` AFTER UPDATE ON `hospitaldata` FOR EACH ROW INSERT INTO triger VALUES(null,NEW.HosCode,NEW.normalbed,NEW.icubed,NEW.ventbed,'UPDATED',NOW())
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `hospitaluser`
--

CREATE TABLE `hospitaluser` (
  `id` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `HosCode` varchar(100) NOT NULL,
  `password` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `hospitaluser`
--

INSERT INTO `hospitaluser` (`id`, `email`, `HosCode`, `password`) VALUES
(1, 'hospital1@gmail.com', 'H101', 'pbkdf2:sha256:260000$MrFa1Iv3ac6HMEcE$baebf6109892ac00aa11f68a04ffb8841b707940c15ec0d3e6214bf91daa02a9'),
(2, 'hospital2@gmail.com', 'H102', 'pbkdf2:sha256:260000$heAcmLrTW2guneIU$6491d1dd41e08675b05162fd21a8656570a35d54d56252089dff891ba3891efc');

-- --------------------------------------------------------

--
-- Table structure for table `test`
--

CREATE TABLE `test` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `triger`
--

CREATE TABLE `triger` (
  `id` int(11) NOT NULL,
  `HosCode` varchar(100) NOT NULL,
  `normalbed` int(11) NOT NULL,
  `icubed` int(11) NOT NULL,
  `ventbed` int(11) NOT NULL,
  `querys` varchar(50) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `triger`
--

INSERT INTO `triger` (`id`, `HosCode`, `normalbed`, `icubed`, `ventbed`, `querys`, `date`) VALUES
(1, 'H101', 24, 7, 10, 'UPDATED', '2022-05-30'),
(2, 'H101', 24, 7, 10, 'DELETED', '2022-05-30'),
(3, 'H101 ', 50, 30, 15, 'INSERTED', '2022-05-30'),
(4, 'H102 ', 35, 12, 15, 'UPDATED', '2022-05-31'),
(5, 'H101 ', 50, 30, 15, 'UPDATED', '2022-05-31');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bookingbed`
--
ALTER TABLE `bookingbed`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `hospitaldata`
--
ALTER TABLE `hospitaldata`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `HosCode` (`HosCode`);

--
-- Indexes for table `hospitaluser`
--
ALTER TABLE `hospitaluser`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `HosCode` (`HosCode`);

--
-- Indexes for table `test`
--
ALTER TABLE `test`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `triger`
--
ALTER TABLE `triger`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bookingbed`
--
ALTER TABLE `bookingbed`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `hospitaldata`
--
ALTER TABLE `hospitaldata`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `hospitaluser`
--
ALTER TABLE `hospitaluser`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `test`
--
ALTER TABLE `test`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `triger`
--
ALTER TABLE `triger`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
