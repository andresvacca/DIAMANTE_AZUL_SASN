-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         11.4.10-MariaDB - MariaDB Server
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.17.0.7270
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para diamante_azul
CREATE DATABASE IF NOT EXISTS `diamante_azul` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `diamante_azul`;

-- Volcando estructura para tabla diamante_azul.articulos
CREATE TABLE IF NOT EXISTS `articulos` (
  `id_articulo` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` longtext DEFAULT NULL,
  `numero_serie` varchar(50) DEFAULT NULL,
  `categoria` varchar(20) DEFAULT NULL,
  `estado` varchar(10) NOT NULL,
  `precio_sugerido_venta` decimal(10,2) NOT NULL,
  `quilataje` enum('0','10','14','16','18') DEFAULT NULL,
  PRIMARY KEY (`id_articulo`)
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.articulos: ~77 rows (aproximadamente)
INSERT INTO `articulos` (`id_articulo`, `nombre`, `descripcion`, `numero_serie`, `categoria`, `estado`, `precio_sugerido_venta`, `quilataje`) VALUES
	(2, 'asdasda', 'asrwerwe', '1231233', 'Computadores', 'Vencido', 55000.00, '0'),
	(3, 'anillo', 'asrasd', '1231', 'Ollas', 'Vencido', 33000.00, '0'),
	(4, 'Bicicleta TT On Drive', 'ASKJDGASKDHAKSJHDGASKHJD', '1213112432', 'Bicicletas', 'Vencido', 143000.00, '0'),
	(5, 'dwrfsdf', '1232123', '123123', 'VideoJuegos', 'Vencido', 135678.40, '0'),
	(6, 'celulcar', 'oppo 56', '12345', 'Otro', 'Empeñado', 10000000.00, '0'),
	(7, 'celular', 'oppo 56', '12345', 'Otro', 'Empeñado', 10000000.00, '0'),
	(8, 'celular', 'oppo 56', '12345', 'Otro', 'Vencido', 1100000.00, '0'),
	(9, 'guallando', 'kjhsdfksdjnfksdjh', '1231234', 'Relojes', 'Empeñado', 55000.00, '0'),
	(10, 'Bicicleta Trek', 'Bicicleta de montaña azul', 'TRK-001', 'Bicicletas', 'En venta', 350000.00, '0'),
	(11, 'Nevera Samsung', 'Nevera 300L gris', 'SAM-NVR-002', 'Neveras', 'En venta', 800000.00, '0'),
	(12, 'Anillo de Oro', 'Anillo de oro 18k con piedra', 'ORO-003', 'Oro', 'Empeñado', 13200.00, '18'),
	(13, 'Reloj Casio', 'Reloj digital negro', 'CAS-004', 'Relojes', 'En venta', 150000.00, '0'),
	(14, 'Computador HP', 'Portátil HP Core i5', 'HP-005', 'Computadores', 'En venta', 1500000.00, '0'),
	(15, 'Bicicleta BMW', 'Bicicleta TT rin 29"', '5414235', 'Bicicletas', 'Empeñado', 55000.00, '0'),
	(16, 'Cadena de Oro', 'Cadena de oro 18k 50cm', 'ORO-CAD-001', 'Oro', 'En venta', 2500000.00, '18'),
	(17, 'PlayStation 5', 'Consola Sony PS5 con dos controles', 'PS5-002', 'VideoJuegos', 'En venta', 3200000.00, '0'),
	(18, 'Lavadora LG', 'Lavadora carga frontal 9kg', 'LG-LAV-003', 'Neveras', 'Empeñado', 550000.00, '0'),
	(19, 'Reloj Fossil', 'Reloj análogo cuero café', 'FOS-004', 'Relojes', 'En venta', 420000.00, '0'),
	(20, 'MacBook Air', 'Portátil Apple M1 8GB RAM', 'MAC-005', 'Computadores', 'En venta', 4800000.00, '0'),
	(21, 'Anillo Plata', 'Anillo de plata con circón', 'PLA-006', 'Plata', 'En venta', 180000.00, '0'),
	(22, 'Bicicleta Gios', 'Bicicleta ruta azul talla M', 'GIO-007', 'Bicicletas', 'En venta', 1100000.00, '0'),
	(23, 'Aretes Oro', 'Aretes de oro 14k con rubí', 'ORO-ARE-008', 'Oro', 'En venta', 890000.00, '14'),
	(24, 'Nintendo Switch', 'Consola Nintendo Switch OLED', 'NIN-009', 'VideoJuegos', 'Empeñado', 330000.00, '0'),
	(25, 'Computador Lenovo', 'PC de escritorio Lenovo i7', 'LEN-010', 'Computadores', 'Empeñado', 143000.00, '0'),
	(26, 'hujosñjdfksf', 'kgjsldfjgjldfgjl', '2342342', 'VideoJuegos', 'Empeñado', 234557.40, '0'),
	(27, 'yupi Tyso', 'skgjdfslgdlgj', '1234567', 'Relojes', 'En venta', 123.00, '0'),
	(28, '[TEST] Bicicleta Trek Montaña', 'Bicicleta de montaña azul 21 velocidades', 'TRK-T001', 'Bicicletas', 'En venta', 350000.00, '0'),
	(29, '[TEST] Bicicleta Specialized Ruta', 'Bicicleta de ruta negra talla M', 'SPC-T002', 'Bicicletas', 'En venta', 480000.00, '0'),
	(30, '[TEST] Bicicleta GW Todoterreno', 'Bicicleta todoterreno gris', 'GW-T003', 'Bicicletas', 'En venta', 290000.00, '0'),
	(31, '[TEST] Bicicleta Shimano Urbana', 'Bicicleta urbana verde con canasta', 'SHM-T004', 'Bicicletas', 'En venta', 220000.00, '0'),
	(32, '[TEST] Nevera Samsung 300L', 'Nevera gris 300 litros No Frost', 'SAM-T005', 'Neveras', 'En venta', 950000.00, '0'),
	(33, '[TEST] Nevera LG Gris 400L', 'Nevera LG 400L doble puerta', 'LG-T006', 'Neveras', 'En venta', 1200000.00, '0'),
	(34, '[TEST] Nevera Haceb 200L', 'Nevera pequeña blanca 200L', 'HAC-T007', 'Neveras', 'En venta', 650000.00, '0'),
	(35, '[TEST] Nevera Mabe Plateada', 'Nevera Mabe 350L plateada', 'MAB-T008', 'Neveras', 'En venta', 880000.00, '0'),
	(36, '[TEST] Anillo Oro 18k Diamante', 'Anillo de oro 18k con diamante central', 'ORO-T009', 'Oro', 'En venta', 2800000.00, '18'),
	(37, '[TEST] Cadena Oro 18k 50cm', 'Cadena de oro 18k 50 centímetros', 'ORO-T010', 'Oro', 'En venta', 2200000.00, '18'),
	(38, '[TEST] Pulsera Oro 14k', 'Pulsera de oro 14k con dije', 'ORO-T011', 'Oro', 'En venta', 1500000.00, '14'),
	(39, '[TEST] Aretes Oro 18k Perla', 'Aretes de oro 18k con perla', 'ORO-T012', 'Oro', 'Empeñado', 110000.00, '18'),
	(40, '[TEST] Anillo Oro 10k Sencillo', 'Anillo liso de oro 10k', 'ORO-T013', 'Oro', 'En venta', 750000.00, '10'),
	(41, '[TEST] Collar Oro 16k Figura', 'Collar de oro 16k con figura corazón', 'ORO-T014', 'Oro', 'En venta', 1100000.00, '16'),
	(42, '[TEST] Anillo Plata 925 Piedra', 'Anillo de plata 925 con piedra azul', 'PLA-T015', 'Plata', 'En venta', 180000.00, '0'),
	(43, '[TEST] Pulsera Plata Eslabón', 'Pulsera de plata eslabón grueso', 'PLA-T016', 'Plata', 'En venta', 150000.00, '0'),
	(44, '[TEST] Aretes Plata Argolla', 'Aretes de plata argolla grande', 'PLA-T017', 'Plata', 'En venta', 90000.00, '0'),
	(45, '[TEST] Collar Plata Ley', 'Collar de plata ley 925', 'PLA-T018', 'Plata', 'En venta', 200000.00, '0'),
	(46, '[TEST] Set Ollas Imusa 9 Piezas', 'Juego de ollas Imusa acero inoxidable', 'IMS-T019', 'Ollas', 'En venta', 320000.00, '0'),
	(47, '[TEST] Set Ollas Umco 7 Piezas', 'Juego de ollas Umco antiadherente', 'UMC-T020', 'Ollas', 'En venta', 280000.00, '0'),
	(48, '[TEST] Olla Presión Caribe 10L', 'Olla a presión Caribe 10 litros', 'CAR-T021', 'Ollas', 'En venta', 150000.00, '0'),
	(49, '[TEST] Set Ollas Haceb Completo', 'Set completo ollas Haceb 12 piezas', 'HAC-T022', 'Ollas', 'En venta', 410000.00, '0'),
	(50, '[TEST] PlayStation 5 Disc', 'Consola Sony PS5 con lector de disco', 'PS5-T023', 'VideoJuegos', 'En venta', 3200000.00, '0'),
	(51, '[TEST] Xbox Series X', 'Consola Microsoft Xbox Series X', 'XBX-T024', 'VideoJuegos', 'En venta', 2900000.00, '0'),
	(52, '[TEST] Nintendo Switch OLED', 'Consola Nintendo Switch OLED blanca', 'NIN-T025', 'VideoJuegos', 'En venta', 1800000.00, '0'),
	(53, '[TEST] PlayStation 4 Pro', 'Consola Sony PS4 Pro 1TB', 'PS4-T026', 'VideoJuegos', 'En venta', 1200000.00, '0'),
	(54, '[TEST] Control PS5 DualSense', 'Control inalámbrico PS5 blanco', 'CTR-T027', 'VideoJuegos', 'En venta', 380000.00, '0'),
	(55, '[TEST] Reloj Casio Digital', 'Reloj Casio digital negro clásico', 'CAS-T028', 'Relojes', 'En venta', 150000.00, '0'),
	(56, '[TEST] Reloj Fossil Cuero', 'Reloj Fossil análogo correa cuero café', 'FOS-T029', 'Relojes', 'En venta', 420000.00, '0'),
	(57, '[TEST] Reloj Citizen Automático', 'Reloj Citizen automático plateado', 'CTZ-T030', 'Relojes', 'En venta', 680000.00, '0'),
	(58, '[TEST] Reloj Seiko 5 Sports', 'Reloj Seiko 5 Sports automático azul', 'SEI-T031', 'Relojes', 'En venta', 550000.00, '0'),
	(59, '[TEST] Reloj Orient Bambino', 'Reloj Orient Bambino dress watch negro', 'ORI-T032', 'Relojes', 'En venta', 490000.00, '0'),
	(60, '[TEST] MacBook Air M1', 'Portátil Apple MacBook Air M1 8GB 256GB', 'MAC-T033', 'Computadores', 'En venta', 4800000.00, '0'),
	(61, '[TEST] MacBook Pro M2', 'Portátil Apple MacBook Pro M2 16GB 512GB', 'MBP-T034', 'Computadores', 'Empeñado', 209000.00, '0'),
	(62, '[TEST] Lenovo IdeaPad i5', 'Portátil Lenovo IdeaPad Core i5 8GB', 'LEN-T035', 'Computadores', 'En venta', 2100000.00, '0'),
	(63, '[TEST] HP Pavilion i7', 'Portátil HP Pavilion Core i7 16GB', 'HPP-T036', 'Computadores', 'En venta', 3100000.00, '0'),
	(64, '[TEST] Dell Inspiron i5', 'Portátil Dell Inspiron Core i5 8GB', 'DEL-T037', 'Computadores', 'En venta', 2400000.00, '0'),
	(65, '[TEST] PC Escritorio Lenovo', 'PC escritorio Lenovo Core i7 16GB', 'PCL-T038', 'Computadores', 'En venta', 2800000.00, '0'),
	(66, '[TEST] Monitor Samsung 24', 'Monitor Samsung 24 pulgadas Full HD', 'MON-T039', 'Computadores', 'En venta', 680000.00, '0'),
	(67, '[TEST] Audífonos Sony WH1000XM4', 'Audífonos Sony con cancelación ruido', 'SNY-T040', 'Otro', 'Empeñado', 1540000.00, '0'),
	(68, '[TEST] Cámara Canon Rebel', 'Cámara réflex Canon Rebel T7 con lente', 'CAN-T041', 'Otro', 'Empeñado', 113300.00, '0'),
	(69, '[TEST] Tablet Samsung Tab A8', 'Tablet Samsung Galaxy Tab A8 64GB', 'TAB-T042', 'Otro', 'En venta', 850000.00, '0'),
	(70, '[TEST] iPhone 13 128GB', 'Smartphone Apple iPhone 13 negro 128GB', 'IPH-T043', 'Otro', 'En venta', 3200000.00, '0'),
	(71, '[TEST] Samsung Galaxy S22', 'Smartphone Samsung Galaxy S22 256GB', 'SAG-T044', 'Otro', 'En venta', 2600000.00, '0'),
	(72, '[TEST] Drone DJI Mini 2', 'Drone DJI Mini 2 con control y estuche', 'DJI-T045', 'Otro', 'En venta', 1900000.00, '0'),
	(73, '[TEST] GoPro Hero 11', 'Cámara acción GoPro Hero 11 Black', 'GPR-T046', 'Otro', 'En venta', 1400000.00, '0'),
	(74, '[TEST] Aspiradora Dyson V11', 'Aspiradora inalámbrica Dyson V11', 'DYS-T047', 'Otro', 'En venta', 2300000.00, '0'),
	(75, '[TEST] Lavadora Samsung 9kg', 'Lavadora Samsung carga frontal 9kg', 'LSA-T048', 'Neveras', 'En venta', 1800000.00, '0'),
	(76, '[TEST] Microondas Haceb 28L', 'Microondas Haceb 28 litros gris', 'MIC-T049', 'Otro', 'En venta', 320000.00, '0'),
	(77, '[TEST] Parlante JBL Charge 5', 'Parlante portátil JBL Charge 5 azul', 'JBL-T050', 'Otro', 'Vencido', 13200000.00, '0'),
	(78, 'barato', 'baratoprueba', '1231231', 'Bicicletas', 'Empeñado', 8800.00, '0'),
	(79, 'baratov2', 'ASDASDASDA', '321123123123', 'Plata', 'En venta', 130.00, '0');

-- Volcando estructura para tabla diamante_azul.auth_group
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.auth_group: ~0 rows (aproximadamente)

-- Volcando estructura para tabla diamante_azul.auth_group_permissions
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.auth_group_permissions: ~0 rows (aproximadamente)

-- Volcando estructura para tabla diamante_azul.auth_permission
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.auth_permission: ~112 rows (aproximadamente)
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
	(1, 'Can add log entry', 1, 'add_logentry'),
	(2, 'Can change log entry', 1, 'change_logentry'),
	(3, 'Can delete log entry', 1, 'delete_logentry'),
	(4, 'Can view log entry', 1, 'view_logentry'),
	(5, 'Can add permission', 2, 'add_permission'),
	(6, 'Can change permission', 2, 'change_permission'),
	(7, 'Can delete permission', 2, 'delete_permission'),
	(8, 'Can view permission', 2, 'view_permission'),
	(9, 'Can add group', 3, 'add_group'),
	(10, 'Can change group', 3, 'change_group'),
	(11, 'Can delete group', 3, 'delete_group'),
	(12, 'Can view group', 3, 'view_group'),
	(13, 'Can add user', 4, 'add_user'),
	(14, 'Can change user', 4, 'change_user'),
	(15, 'Can delete user', 4, 'delete_user'),
	(16, 'Can view user', 4, 'view_user'),
	(17, 'Can add content type', 5, 'add_contenttype'),
	(18, 'Can change content type', 5, 'change_contenttype'),
	(19, 'Can delete content type', 5, 'delete_contenttype'),
	(20, 'Can view content type', 5, 'view_contenttype'),
	(21, 'Can add session', 6, 'add_session'),
	(22, 'Can change session', 6, 'change_session'),
	(23, 'Can delete session', 6, 'delete_session'),
	(24, 'Can view session', 6, 'view_session'),
	(25, 'Can add articulos', 7, 'add_articulos'),
	(26, 'Can change articulos', 7, 'change_articulos'),
	(27, 'Can delete articulos', 7, 'delete_articulos'),
	(28, 'Can view articulos', 7, 'view_articulos'),
	(29, 'Can add cliente', 8, 'add_cliente'),
	(30, 'Can change cliente', 8, 'change_cliente'),
	(31, 'Can delete cliente', 8, 'delete_cliente'),
	(32, 'Can view cliente', 8, 'view_cliente'),
	(33, 'Can add cuota', 9, 'add_cuota'),
	(34, 'Can change cuota', 9, 'change_cuota'),
	(35, 'Can delete cuota', 9, 'delete_cuota'),
	(36, 'Can view cuota', 9, 'view_cuota'),
	(37, 'Can add pago', 10, 'add_pago'),
	(38, 'Can change pago', 10, 'change_pago'),
	(39, 'Can delete pago', 10, 'delete_pago'),
	(40, 'Can view pago', 10, 'view_pago'),
	(41, 'Can add empeno', 11, 'add_empeno'),
	(42, 'Can change empeno', 11, 'change_empeno'),
	(43, 'Can delete empeno', 11, 'delete_empeno'),
	(44, 'Can view empeno', 11, 'view_empeno'),
	(45, 'Can add rol', 12, 'add_rol'),
	(46, 'Can change rol', 12, 'change_rol'),
	(47, 'Can delete rol', 12, 'delete_rol'),
	(48, 'Can view rol', 12, 'view_rol'),
	(49, 'Can add usuario', 13, 'add_usuario'),
	(50, 'Can change usuario', 13, 'change_usuario'),
	(51, 'Can delete usuario', 13, 'delete_usuario'),
	(52, 'Can view usuario', 13, 'view_usuario'),
	(53, 'Can add factura', 14, 'add_factura'),
	(54, 'Can change factura', 14, 'change_factura'),
	(55, 'Can delete factura', 14, 'delete_factura'),
	(56, 'Can view factura', 14, 'view_factura'),
	(57, 'Can add detalle factura', 15, 'add_detallefactura'),
	(58, 'Can change detalle factura', 15, 'change_detallefactura'),
	(59, 'Can delete detalle factura', 15, 'delete_detallefactura'),
	(60, 'Can view detalle factura', 15, 'view_detallefactura'),
	(61, 'Can add contrato', 16, 'add_contrato'),
	(62, 'Can change contrato', 16, 'change_contrato'),
	(63, 'Can delete contrato', 16, 'delete_contrato'),
	(64, 'Can view contrato', 16, 'view_contrato'),
	(65, 'Can add crontab', 17, 'add_crontabschedule'),
	(66, 'Can change crontab', 17, 'change_crontabschedule'),
	(67, 'Can delete crontab', 17, 'delete_crontabschedule'),
	(68, 'Can view crontab', 17, 'view_crontabschedule'),
	(69, 'Can add interval', 18, 'add_intervalschedule'),
	(70, 'Can change interval', 18, 'change_intervalschedule'),
	(71, 'Can delete interval', 18, 'delete_intervalschedule'),
	(72, 'Can view interval', 18, 'view_intervalschedule'),
	(73, 'Can add periodic task', 19, 'add_periodictask'),
	(74, 'Can change periodic task', 19, 'change_periodictask'),
	(75, 'Can delete periodic task', 19, 'delete_periodictask'),
	(76, 'Can view periodic task', 19, 'view_periodictask'),
	(77, 'Can add periodic task track', 20, 'add_periodictasks'),
	(78, 'Can change periodic task track', 20, 'change_periodictasks'),
	(79, 'Can delete periodic task track', 20, 'delete_periodictasks'),
	(80, 'Can view periodic task track', 20, 'view_periodictasks'),
	(81, 'Can add solar event', 21, 'add_solarschedule'),
	(82, 'Can change solar event', 21, 'change_solarschedule'),
	(83, 'Can delete solar event', 21, 'delete_solarschedule'),
	(84, 'Can view solar event', 21, 'view_solarschedule'),
	(85, 'Can add clocked', 22, 'add_clockedschedule'),
	(86, 'Can change clocked', 22, 'change_clockedschedule'),
	(87, 'Can delete clocked', 22, 'delete_clockedschedule'),
	(88, 'Can view clocked', 22, 'view_clockedschedule'),
	(89, 'Can add task result', 23, 'add_taskresult'),
	(90, 'Can change task result', 23, 'change_taskresult'),
	(91, 'Can delete task result', 23, 'delete_taskresult'),
	(92, 'Can view task result', 23, 'view_taskresult'),
	(93, 'Can add chord counter', 24, 'add_chordcounter'),
	(94, 'Can change chord counter', 24, 'change_chordcounter'),
	(95, 'Can delete chord counter', 24, 'delete_chordcounter'),
	(96, 'Can view chord counter', 24, 'view_chordcounter'),
	(97, 'Can add group result', 25, 'add_groupresult'),
	(98, 'Can change group result', 25, 'change_groupresult'),
	(99, 'Can delete group result', 25, 'delete_groupresult'),
	(100, 'Can view group result', 25, 'view_groupresult'),
	(101, 'Can add compra', 26, 'add_compra'),
	(102, 'Can change compra', 26, 'change_compra'),
	(103, 'Can delete compra', 26, 'delete_compra'),
	(104, 'Can view compra', 26, 'view_compra'),
	(105, 'Can add notificacion', 27, 'add_notificacion'),
	(106, 'Can change notificacion', 27, 'change_notificacion'),
	(107, 'Can delete notificacion', 27, 'delete_notificacion'),
	(108, 'Can view notificacion', 27, 'view_notificacion'),
	(109, 'Can add venta articulo', 28, 'add_ventaarticulo'),
	(110, 'Can change venta articulo', 28, 'change_ventaarticulo'),
	(111, 'Can delete venta articulo', 28, 'delete_ventaarticulo'),
	(112, 'Can view venta articulo', 28, 'view_ventaarticulo');

-- Volcando estructura para tabla diamante_azul.auth_user
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.auth_user: ~1 rows (aproximadamente)
INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
	(1, 'pbkdf2_sha256$600000$LKjmsx62K2qOHeDkFOKvkQ$EuEidKBXo4/ULKUADoPffh90/vChsRjda2JgvmMnY0M=', '2026-04-23 20:46:31.538945', 1, 'AndresV', '', '', 'avacca853@gmail.com', 1, 1, '2026-04-23 20:46:18.663674'),
	(2, 'pbkdf2_sha256$600000$tdalUzV1Q7If7DWMfdcFEY$ZjTqmVJCzxtNFWRYXVslEReyH25T0kvPxWRIFGuA+YE=', '2026-04-23 21:24:36.396252', 1, 'Vaquita', '', '', 'avacca853@gmail.com', 1, 1, '2026-04-23 21:24:15.542938');

-- Volcando estructura para tabla diamante_azul.auth_user_groups
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.auth_user_groups: ~0 rows (aproximadamente)

-- Volcando estructura para tabla diamante_azul.auth_user_user_permissions
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.auth_user_user_permissions: ~0 rows (aproximadamente)

-- Volcando estructura para tabla diamante_azul.clientes
CREATE TABLE IF NOT EXISTS `clientes` (
  `id_cliente` int(11) NOT NULL AUTO_INCREMENT,
  `documento_id` varchar(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` longtext DEFAULT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `lugar_expedicion` varchar(100) DEFAULT NULL,
  `departamento_expedicion` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_cliente`),
  UNIQUE KEY `documento_id` (`documento_id`),
  UNIQUE KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `clientes_cliente_id_usuario_7e20470f_fk_usuarios_` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios_usuario` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.clientes: ~13 rows (aproximadamente)
INSERT INTO `clientes` (`id_cliente`, `documento_id`, `nombre`, `telefono`, `direccion`, `id_usuario`, `lugar_expedicion`, `departamento_expedicion`) VALUES
	(2, '1111111111111', 'Andres Guayabo', '301987624', 'busca ppp', 4, NULL, NULL),
	(4, '1456789002131', 'tulio', '314567894', 'prueba6@gmail.com', 6, NULL, NULL),
	(8, '11111111111112', 'aaaaaaaaaaa', '22222222222', 'aasdwea', 12, NULL, NULL),
	(9, '56789454', 'Yulieth', '12313423', 'Bosa Independencia', 13, NULL, NULL),
	(10, '11141320744', 'nicolas', '3150658900', '', 15, 'Puerto Santander', 'AMAZONAS'),
	(11, '5447656896', 'jhjyjjjjjj', '768687568', 'ghgg', 16, NULL, NULL),
	(12, '242344234', 'bueno', '2393747887', 'vumjek', 17, 'Cachipay', 'CUNDINAMARCA'),
	(13, '5734386', 'Andres Felipe Vacca', '1234567890', 'jgdfldkj', 18, 'Sabanalarga', 'CASANARE'),
	(14, '564563456', 'FDSFDSFSF', '342342123', 'SDLFSDFSDFSDASDA', 19, 'Argelia', 'CAUCA'),
	(15, '1132456786', 'pruebaNoti', '12314123423', 'Prueba Noti', 21, 'Riohacha', 'LA GUAJIRA'),
	(16, '132123123', 'prueba2', '13413423', 'Prueba Noti 2', 22, 'Cacahual', 'GUAINÍA'),
	(17, '123456878', '[TEST]', '42342324', 'dsfddsfdfgdfgdfg', 23, 'Cachipay', 'CUNDINAMARCA'),
	(18, '99999999', 'Javier', '3026075362', 'admin@gmai.com', 24, 'Bojacá', 'CUNDINAMARCA');

-- Volcando estructura para tabla diamante_azul.compra
CREATE TABLE IF NOT EXISTS `compra` (
  `id_compra` int(11) NOT NULL AUTO_INCREMENT,
  `fecha_compra` date NOT NULL,
  `precio_pagado` decimal(12,2) NOT NULL,
  `precio_reventa` decimal(12,2) NOT NULL,
  `estado` varchar(15) NOT NULL,
  `id_articulo_id` int(11) NOT NULL,
  `id_cliente_id` int(11) NOT NULL,
  `id_factura_compra_id` int(11) DEFAULT NULL,
  `id_factura_venta_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_compra`),
  UNIQUE KEY `id_factura_compra_id` (`id_factura_compra_id`),
  UNIQUE KEY `id_factura_venta_id` (`id_factura_venta_id`),
  KEY `compra_id_articulo_id_0fbb4943_fk_articulos_id_articulo` (`id_articulo_id`),
  KEY `compra_id_cliente_id_5f3c144a_fk_clientes_id_cliente` (`id_cliente_id`),
  CONSTRAINT `compra_id_articulo_id_0fbb4943_fk_articulos_id_articulo` FOREIGN KEY (`id_articulo_id`) REFERENCES `articulos` (`id_articulo`),
  CONSTRAINT `compra_id_cliente_id_5f3c144a_fk_clientes_id_cliente` FOREIGN KEY (`id_cliente_id`) REFERENCES `clientes` (`id_cliente`),
  CONSTRAINT `compra_id_factura_compra_id_56bf0b52_fk_facturas_id_factura` FOREIGN KEY (`id_factura_compra_id`) REFERENCES `facturas` (`id_factura`),
  CONSTRAINT `compra_id_factura_venta_id_232207e5_fk_facturas_id_factura` FOREIGN KEY (`id_factura_venta_id`) REFERENCES `facturas` (`id_factura`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.compra: ~3 rows (aproximadamente)
INSERT INTO `compra` (`id_compra`, `fecha_compra`, `precio_pagado`, `precio_reventa`, `estado`, `id_articulo_id`, `id_cliente_id`, `id_factura_compra_id`, `id_factura_venta_id`) VALUES
	(3, '2026-03-27', 100.00, 200.00, 'Vendido', 5, 2, 9, NULL),
	(4, '2026-04-03', 1234567.00, 12345678.00, 'Vendido', 16, 10, 12, NULL),
	(5, '2026-04-03', 123423.00, 123145.00, 'Vendido', 27, 10, 14, NULL);

-- Volcando estructura para tabla diamante_azul.compras_ventaarticulo
CREATE TABLE IF NOT EXISTS `compras_ventaarticulo` (
  `id_venta` int(11) NOT NULL AUTO_INCREMENT,
  `precio_venta_final` decimal(12,2) NOT NULL,
  `utilidad_generada` decimal(12,2) DEFAULT NULL,
  `id_compra_id` int(11) NOT NULL,
  `id_factura_id` int(11) NOT NULL,
  PRIMARY KEY (`id_venta`),
  UNIQUE KEY `id_factura_id` (`id_factura_id`),
  KEY `venta_articulo_id_compra_id_9ec3ab40_fk_compra_id_compra` (`id_compra_id`),
  CONSTRAINT `venta_articulo_id_compra_id_9ec3ab40_fk_compra_id_compra` FOREIGN KEY (`id_compra_id`) REFERENCES `compra` (`id_compra`),
  CONSTRAINT `venta_articulo_id_factura_id_fbe25e5b_fk_facturas_id_factura` FOREIGN KEY (`id_factura_id`) REFERENCES `facturas` (`id_factura`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.compras_ventaarticulo: ~3 rows (aproximadamente)
INSERT INTO `compras_ventaarticulo` (`id_venta`, `precio_venta_final`, `utilidad_generada`, `id_compra_id`, `id_factura_id`) VALUES
	(1, 123145.00, -278.00, 5, 19),
	(2, 12345678.00, 11111111.00, 4, 20),
	(3, 200.00, 100.00, 3, 21);

-- Volcando estructura para tabla diamante_azul.contrato
CREATE TABLE IF NOT EXISTS `contrato` (
  `id_contrato` int(11) NOT NULL AUTO_INCREMENT,
  `fecha_contrato` date NOT NULL,
  `tipo_contrato` varchar(20) DEFAULT NULL,
  `estado_contrato` varchar(10) DEFAULT NULL,
  `id_articulo_id` int(11) NOT NULL,
  `id_cliente_id` int(11) NOT NULL,
  `id_cuota_id` int(11) DEFAULT NULL,
  `id_empeno_id` int(11) DEFAULT NULL,
  `id_factura_id` int(11) DEFAULT NULL,
  `id_pago_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_contrato`),
  KEY `contrato_id_articulo_id_2523db23_fk_articulos_id_articulo` (`id_articulo_id`),
  KEY `contrato_id_cliente_id_abf71478_fk_clientes_cliente_id_cliente` (`id_cliente_id`),
  KEY `contrato_id_cuota_id_ce628efc_fk_cuotas_id_cuota` (`id_cuota_id`),
  KEY `contrato_id_empeno_id_b78f092d_fk_empenos_id_empeno` (`id_empeno_id`),
  KEY `contrato_id_factura_id_23c254b3_fk_facturas_id_factura` (`id_factura_id`),
  KEY `contrato_id_pago_id_2d3f5c7a_fk_pagos_id_pago` (`id_pago_id`),
  CONSTRAINT `contrato_id_articulo_id_2523db23_fk_articulos_id_articulo` FOREIGN KEY (`id_articulo_id`) REFERENCES `articulos` (`id_articulo`),
  CONSTRAINT `contrato_id_cliente_id_abf71478_fk_clientes_cliente_id_cliente` FOREIGN KEY (`id_cliente_id`) REFERENCES `clientes` (`id_cliente`),
  CONSTRAINT `contrato_id_cuota_id_ce628efc_fk_cuotas_id_cuota` FOREIGN KEY (`id_cuota_id`) REFERENCES `cuotas` (`id_cuota`),
  CONSTRAINT `contrato_id_empeno_id_b78f092d_fk_empenos_id_empeno` FOREIGN KEY (`id_empeno_id`) REFERENCES `empenos` (`id_empeno`),
  CONSTRAINT `contrato_id_factura_id_23c254b3_fk_facturas_id_factura` FOREIGN KEY (`id_factura_id`) REFERENCES `facturas` (`id_factura`),
  CONSTRAINT `contrato_id_pago_id_2d3f5c7a_fk_pagos_id_pago` FOREIGN KEY (`id_pago_id`) REFERENCES `pagos` (`id_pago`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.contrato: ~35 rows (aproximadamente)
INSERT INTO `contrato` (`id_contrato`, `fecha_contrato`, `tipo_contrato`, `estado_contrato`, `id_articulo_id`, `id_cliente_id`, `id_cuota_id`, `id_empeno_id`, `id_factura_id`, `id_pago_id`) VALUES
	(1, '2026-03-25', 'Normal', 'Disponible', 3, 2, 5, 3, NULL, NULL),
	(2, '2026-03-25', 'Normal', 'Disponible', 3, 2, 5, 3, NULL, NULL),
	(3, '2026-03-25', 'Plazo Maximo', 'Disponible', 4, 2, 5, 6, NULL, NULL),
	(4, '2026-03-25', 'Normal', 'Disponible', 5, 8, 6, 7, NULL, NULL),
	(5, '2026-03-27', 'Normal', 'Disponible', 15, 11, 8, 10, NULL, NULL),
	(6, '2026-04-01', 'Contrato sobre Oro', 'Disponible', 12, 9, NULL, 12, NULL, NULL),
	(7, '2026-04-01', 'Normal', 'Disponible', 8, 9, NULL, 8, NULL, NULL),
	(8, '2026-04-02', 'Plazo Maximo', 'Disponible', 25, 11, NULL, 11, NULL, NULL),
	(9, '2026-04-02', 'Plazo Maximo', 'Disponible', 26, 4, NULL, 13, NULL, NULL),
	(10, '2026-04-08', 'Normal', 'Disponible', 18, 13, NULL, 14, NULL, NULL),
	(11, '2026-04-08', 'Normal', 'Disponible', 24, 13, NULL, 15, NULL, NULL),
	(12, '2026-04-08', 'Normal   ', 'Disponible', 24, 13, NULL, 15, NULL, NULL),
	(13, '2026-04-10', 'Normal', 'Disponible', 68, 18, NULL, 16, NULL, NULL),
	(14, '2026-04-10', 'Normal', 'Disponible', 68, 18, NULL, 16, NULL, NULL),
	(15, '2026-04-10', 'Normal', 'Disponible', 77, 18, NULL, 17, NULL, NULL),
	(16, '2026-04-10', 'Normal', 'Disponible', 77, 18, NULL, 17, NULL, NULL),
	(17, '2026-04-11', 'Normal', 'Disponible', 61, 17, NULL, 18, NULL, NULL),
	(18, '2026-04-12', 'Normal', 'Disponible', 61, 17, NULL, 18, NULL, NULL),
	(19, '2026-04-16', 'Normal', 'Disponible', 68, 18, NULL, 16, NULL, NULL),
	(20, '2026-04-10', 'Normal', 'Disponible', 77, 18, NULL, 17, NULL, NULL),
	(21, '2026-03-13', 'Normal', 'Disponible', 2, 2, NULL, 2, NULL, NULL),
	(22, '2026-04-23', 'Normal', 'Disponible', 67, 15, NULL, 19, NULL, NULL),
	(23, '2026-04-24', 'Plazo Maximo', 'Disponible', 67, 15, NULL, 19, NULL, NULL),
	(24, '2026-04-23', 'Normal', 'Disponible', 39, 12, NULL, 20, NULL, NULL),
	(25, '2026-04-24', 'Contrato sobre Oro', 'Disponible', 39, 12, NULL, 20, NULL, NULL),
	(26, '2026-04-23', 'Normal', 'Disponible', 77, 8, NULL, 21, NULL, NULL),
	(27, '2026-04-24', 'Plazo Maximo', 'Disponible', 77, 8, NULL, 21, NULL, NULL),
	(28, '2026-04-23', 'Normal', 'Disponible', 78, 12, NULL, 22, NULL, NULL),
	(29, '2026-04-24', 'Plazo Maximo', 'Disponible', 78, 12, NULL, 22, NULL, NULL),
	(30, '2026-04-23', 'Normal', 'Disponible', 79, 4, NULL, 23, NULL, NULL),
	(31, '2026-04-24', 'Plazo Maximo', 'Disponible', 79, 4, NULL, 23, NULL, NULL),
	(32, '2026-04-23', 'Normal', 'Disponible', 79, 4, NULL, 24, NULL, NULL),
	(33, '2026-04-24', 'Plazo Maximo', 'Disponible', 79, 4, NULL, 24, NULL, NULL),
	(34, '2026-04-23', 'Normal', 'Disponible', 79, 4, NULL, 25, NULL, NULL),
	(35, '2026-04-24', 'Plazo Maximo', 'Disponible', 79, 4, NULL, 25, NULL, NULL);

-- Volcando estructura para tabla diamante_azul.cuotas
CREATE TABLE IF NOT EXISTS `cuotas` (
  `id_cuota` int(11) NOT NULL AUTO_INCREMENT,
  `numero_cuota` int(11) NOT NULL,
  `fecha_programada` date NOT NULL,
  `capital` decimal(10,2) NOT NULL,
  `interes` decimal(10,2) NOT NULL,
  `mora` decimal(10,2) NOT NULL,
  `estado` varchar(10) NOT NULL,
  `id_empeno_id` int(11) NOT NULL,
  `id_cliente_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_cuota`),
  KEY `cuotas_id_empeno_id_b1659ec3_fk_empenos_id_empeno` (`id_empeno_id`),
  KEY `cuotas_id_cliente_id_78075797_fk_clientes_id_cliente` (`id_cliente_id`),
  CONSTRAINT `cuotas_id_cliente_id_78075797_fk_clientes_id_cliente` FOREIGN KEY (`id_cliente_id`) REFERENCES `clientes` (`id_cliente`),
  CONSTRAINT `cuotas_id_empeno_id_b1659ec3_fk_empenos_id_empeno` FOREIGN KEY (`id_empeno_id`) REFERENCES `empenos` (`id_empeno`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.cuotas: ~32 rows (aproximadamente)
INSERT INTO `cuotas` (`id_cuota`, `numero_cuota`, `fecha_programada`, `capital`, `interes`, `mora`, `estado`, `id_empeno_id`, `id_cliente_id`) VALUES
	(1, 1, '2026-03-13', 50000.00, 5000.00, 0.00, 'Pagada', 2, 2),
	(2, 1, '2026-03-16', 30000.00, 3000.00, 0.00, 'Pagada', 3, 2),
	(3, 1, '2026-04-16', 130000.00, 13000.00, 0.00, 'Pagada', 6, 8),
	(4, 1, '2026-04-17', 123344.00, 12334.40, 0.00, 'Pagada', 7, 2),
	(5, 1, '2026-04-18', 1000000.00, 100000.00, 0.00, 'Pagada', 8, 8),
	(6, 1, '2026-04-24', 50000.00, 5000.00, 0.00, 'Pagada', 9, 9),
	(7, 2, '2026-03-24', 50000.00, 5000.00, 0.00, 'Pagada', 9, 8),
	(8, 1, '2026-04-27', 50000.00, 5000.00, 0.00, 'Pagada', 10, NULL),
	(9, 1, '2026-04-27', 130000.00, 13000.00, 0.00, 'Pagada', 11, NULL),
	(10, 1, '2026-05-01', 12000.00, 1200.00, 0.00, 'Pagada', 12, NULL),
	(11, 1, '2026-05-02', 213234.00, 21323.40, 0.00, 'Pagada', 13, NULL),
	(12, 1, '2026-05-08', 500000.00, 50000.00, 0.00, 'Pagada', 14, NULL),
	(13, 1, '2026-05-08', 300000.00, 30000.00, 0.00, 'Pagada', 15, NULL),
	(14, 1, '2026-05-10', 123000.00, 12300.00, 0.00, 'Pagada', 16, NULL),
	(15, 1, '2026-07-10', 10000000.00, 1000000.00, 0.00, 'Pagada', 17, NULL),
	(16, 1, '2026-05-12', 0.00, 19000.00, 0.00, 'Pagada', 18, NULL),
	(18, 2, '2026-06-09', 0.00, 12300.00, 0.00, 'Pagada', 16, 18),
	(19, 3, '2026-07-09', 0.00, 12300.00, 0.00, 'Pagada', 16, 18),
	(20, 4, '2026-08-08', 0.00, 12300.00, 0.00, 'Pagada', 16, 18),
	(21, 5, '2026-09-07', 0.00, 12300.00, 0.00, 'Pagada', 16, 18),
	(22, 2, '2026-04-15', 0.00, 3000.00, 0.00, 'Pagada', 3, 2),
	(23, 3, '2026-05-15', 0.00, 3000.00, 0.00, 'Pagada', 3, 2),
	(24, 4, '2026-06-14', 0.00, 3000.00, 0.00, 'Pagada', 3, 2),
	(25, 5, '2026-07-14', 0.00, 3000.00, 0.00, 'Pagada', 3, 2),
	(26, 2, '2026-05-18', 0.00, 100000.00, 0.00, 'Pagada', 8, 9),
	(27, 3, '2026-06-17', 0.00, 100000.00, 0.00, 'Pagada', 8, 9),
	(28, 4, '2026-07-17', 0.00, 100000.00, 0.00, 'Pagada', 8, 9),
	(29, 2, '2026-04-12', 0.00, 5000.00, 0.00, 'Pagada', 2, 2),
	(30, 1, '2026-05-23', 0.00, 140000.00, 0.00, 'Pendiente', 19, NULL),
	(31, 1, '2026-05-23', 0.00, 10000.00, 0.00, 'Pendiente', 20, NULL),
	(32, 1, '2026-04-23', 0.00, 1200000.00, 0.00, 'Vencida', 21, NULL),
	(33, 1, '2026-05-23', 0.00, 800.00, 0.00, 'Pendiente', 22, NULL);

-- Volcando estructura para tabla diamante_azul.detalle_factura
CREATE TABLE IF NOT EXISTS `detalle_factura` (
  `id_detalle` int(11) NOT NULL AUTO_INCREMENT,
  `precio_venta` decimal(10,2) NOT NULL,
  `id_articulo_id` int(11) NOT NULL,
  `id_factura_id` int(11) NOT NULL,
  PRIMARY KEY (`id_detalle`),
  KEY `detalle_factura_id_factura_id_768996d7_fk_facturas_id_factura` (`id_factura_id`),
  KEY `detalle_factura_id_articulo_id_8ce27b3e` (`id_articulo_id`),
  CONSTRAINT `detalle_factura_id_articulo_id_8ce27b3e_fk_articulos_id_articulo` FOREIGN KEY (`id_articulo_id`) REFERENCES `articulos` (`id_articulo`),
  CONSTRAINT `detalle_factura_id_factura_id_768996d7_fk_facturas_id_factura` FOREIGN KEY (`id_factura_id`) REFERENCES `facturas` (`id_factura`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.detalle_factura: ~8 rows (aproximadamente)
INSERT INTO `detalle_factura` (`id_detalle`, `precio_venta`, `id_articulo_id`, `id_factura_id`) VALUES
	(2, 1999999.00, 7, 2),
	(3, 1000000.00, 13, 3),
	(9, 100.00, 5, 9),
	(12, 1234567.00, 16, 12),
	(14, 123423.00, 27, 14),
	(19, 123145.00, 27, 19),
	(20, 12345678.00, 16, 20),
	(21, 200.00, 5, 21);

-- Volcando estructura para tabla diamante_azul.django_admin_log
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.django_admin_log: ~0 rows (aproximadamente)
INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
	(1, '2026-04-23 21:40:51.534782', '17', 'Cuota 1 - Empeño 16', 3, '', 9, 2);

-- Volcando estructura para tabla diamante_azul.django_celery_beat_clockedschedule
CREATE TABLE IF NOT EXISTS `django_celery_beat_clockedschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `clocked_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.django_celery_beat_clockedschedule: ~0 rows (aproximadamente)

-- Volcando estructura para tabla diamante_azul.django_celery_beat_crontabschedule
CREATE TABLE IF NOT EXISTS `django_celery_beat_crontabschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `minute` varchar(240) NOT NULL,
  `hour` varchar(96) NOT NULL,
  `day_of_week` varchar(64) NOT NULL,
  `day_of_month` varchar(124) NOT NULL,
  `month_of_year` varchar(64) NOT NULL,
  `timezone` varchar(63) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.django_celery_beat_crontabschedule: ~2 rows (aproximadamente)
INSERT INTO `django_celery_beat_crontabschedule` (`id`, `minute`, `hour`, `day_of_week`, `day_of_month`, `month_of_year`, `timezone`) VALUES
	(1, '0', '8', '*', '1', '*', 'UTC'),
	(2, '0', '4', '*', '*', '*', 'America/Bogota');

-- Volcando estructura para tabla diamante_azul.django_celery_beat_intervalschedule
CREATE TABLE IF NOT EXISTS `django_celery_beat_intervalschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `every` int(11) NOT NULL,
  `period` varchar(24) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.django_celery_beat_intervalschedule: ~0 rows (aproximadamente)

-- Volcando estructura para tabla diamante_azul.django_celery_beat_periodictask
CREATE TABLE IF NOT EXISTS `django_celery_beat_periodictask` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `task` varchar(200) NOT NULL,
  `args` longtext NOT NULL,
  `kwargs` longtext NOT NULL,
  `queue` varchar(200) DEFAULT NULL,
  `exchange` varchar(200) DEFAULT NULL,
  `routing_key` varchar(200) DEFAULT NULL,
  `expires` datetime(6) DEFAULT NULL,
  `enabled` tinyint(1) NOT NULL,
  `last_run_at` datetime(6) DEFAULT NULL,
  `total_run_count` int(10) unsigned NOT NULL CHECK (`total_run_count` >= 0),
  `date_changed` datetime(6) NOT NULL,
  `description` longtext NOT NULL,
  `crontab_id` int(11) DEFAULT NULL,
  `interval_id` int(11) DEFAULT NULL,
  `solar_id` int(11) DEFAULT NULL,
  `one_off` tinyint(1) NOT NULL,
  `start_time` datetime(6) DEFAULT NULL,
  `priority` int(10) unsigned DEFAULT NULL CHECK (`priority` >= 0),
  `headers` longtext NOT NULL,
  `clocked_id` int(11) DEFAULT NULL,
  `expire_seconds` int(10) unsigned DEFAULT NULL CHECK (`expire_seconds` >= 0),
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `django_celery_beat_p_crontab_id_d3cba168_fk_django_ce` (`crontab_id`),
  KEY `django_celery_beat_p_interval_id_a8ca27da_fk_django_ce` (`interval_id`),
  KEY `django_celery_beat_p_solar_id_a87ce72c_fk_django_ce` (`solar_id`),
  KEY `django_celery_beat_p_clocked_id_47a69f82_fk_django_ce` (`clocked_id`),
  CONSTRAINT `django_celery_beat_p_clocked_id_47a69f82_fk_django_ce` FOREIGN KEY (`clocked_id`) REFERENCES `django_celery_beat_clockedschedule` (`id`),
  CONSTRAINT `django_celery_beat_p_crontab_id_d3cba168_fk_django_ce` FOREIGN KEY (`crontab_id`) REFERENCES `django_celery_beat_crontabschedule` (`id`),
  CONSTRAINT `django_celery_beat_p_interval_id_a8ca27da_fk_django_ce` FOREIGN KEY (`interval_id`) REFERENCES `django_celery_beat_intervalschedule` (`id`),
  CONSTRAINT `django_celery_beat_p_solar_id_a87ce72c_fk_django_ce` FOREIGN KEY (`solar_id`) REFERENCES `django_celery_beat_solarschedule` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.django_celery_beat_periodictask: ~2 rows (aproximadamente)
INSERT INTO `django_celery_beat_periodictask` (`id`, `name`, `task`, `args`, `kwargs`, `queue`, `exchange`, `routing_key`, `expires`, `enabled`, `last_run_at`, `total_run_count`, `date_changed`, `description`, `crontab_id`, `interval_id`, `solar_id`, `one_off`, `start_time`, `priority`, `headers`, `clocked_id`, `expire_seconds`) VALUES
	(1, 'Generar cuotas mensuales', 'empenos.tasks.generar_cuotas_mensuales', '[]', '{}', NULL, NULL, NULL, NULL, 1, NULL, 0, '2026-03-24 00:46:59.777058', '', 1, NULL, NULL, 0, NULL, NULL, '{}', NULL, NULL),
	(2, 'celery.backend_cleanup', 'celery.backend_cleanup', '[]', '{}', NULL, NULL, NULL, NULL, 1, NULL, 0, '2026-03-24 22:35:10.787768', '', 2, NULL, NULL, 0, NULL, NULL, '{}', NULL, 43200);

-- Volcando estructura para tabla diamante_azul.django_celery_beat_periodictasks
CREATE TABLE IF NOT EXISTS `django_celery_beat_periodictasks` (
  `ident` smallint(6) NOT NULL,
  `last_update` datetime(6) NOT NULL,
  PRIMARY KEY (`ident`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.django_celery_beat_periodictasks: ~1 rows (aproximadamente)
INSERT INTO `django_celery_beat_periodictasks` (`ident`, `last_update`) VALUES
	(1, '2026-03-24 22:35:10.788522');

-- Volcando estructura para tabla diamante_azul.django_celery_beat_solarschedule
CREATE TABLE IF NOT EXISTS `django_celery_beat_solarschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event` varchar(24) NOT NULL,
  `latitude` decimal(9,6) NOT NULL,
  `longitude` decimal(9,6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_celery_beat_solar_event_latitude_longitude_ba64999a_uniq` (`event`,`latitude`,`longitude`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.django_celery_beat_solarschedule: ~0 rows (aproximadamente)

-- Volcando estructura para tabla diamante_azul.django_celery_results_chordcounter
CREATE TABLE IF NOT EXISTS `django_celery_results_chordcounter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` varchar(255) NOT NULL,
  `sub_tasks` longtext NOT NULL,
  `count` int(10) unsigned NOT NULL CHECK (`count` >= 0),
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.django_celery_results_chordcounter: ~0 rows (aproximadamente)

-- Volcando estructura para tabla diamante_azul.django_celery_results_groupresult
CREATE TABLE IF NOT EXISTS `django_celery_results_groupresult` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` varchar(255) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_done` datetime(6) NOT NULL,
  `content_type` varchar(128) NOT NULL,
  `content_encoding` varchar(64) NOT NULL,
  `result` longtext DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`),
  KEY `django_cele_date_cr_bd6c1d_idx` (`date_created`),
  KEY `django_cele_date_do_caae0e_idx` (`date_done`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.django_celery_results_groupresult: ~0 rows (aproximadamente)

-- Volcando estructura para tabla diamante_azul.django_celery_results_taskresult
CREATE TABLE IF NOT EXISTS `django_celery_results_taskresult` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` varchar(255) NOT NULL,
  `status` varchar(50) NOT NULL,
  `content_type` varchar(128) NOT NULL,
  `content_encoding` varchar(64) NOT NULL,
  `result` longtext DEFAULT NULL,
  `date_done` datetime(6) NOT NULL,
  `traceback` longtext DEFAULT NULL,
  `meta` longtext DEFAULT NULL,
  `task_args` longtext DEFAULT NULL,
  `task_kwargs` longtext DEFAULT NULL,
  `task_name` varchar(255) DEFAULT NULL,
  `worker` varchar(100) DEFAULT NULL,
  `date_created` datetime(6) NOT NULL,
  `periodic_task_name` varchar(255) DEFAULT NULL,
  `date_started` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_id` (`task_id`),
  KEY `django_cele_task_na_08aec9_idx` (`task_name`),
  KEY `django_cele_status_9b6201_idx` (`status`),
  KEY `django_cele_worker_d54dd8_idx` (`worker`),
  KEY `django_cele_date_cr_f04a50_idx` (`date_created`),
  KEY `django_cele_date_do_f59aad_idx` (`date_done`),
  KEY `django_cele_periodi_1993cf_idx` (`periodic_task_name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.django_celery_results_taskresult: ~10 rows (aproximadamente)
INSERT INTO `django_celery_results_taskresult` (`id`, `task_id`, `status`, `content_type`, `content_encoding`, `result`, `date_done`, `traceback`, `meta`, `task_args`, `task_kwargs`, `task_name`, `worker`, `date_created`, `periodic_task_name`, `date_started`) VALUES
	(1, '26d30da1-32f1-4bde-a543-46aba886a7d5', 'FAILURE', 'application/json', 'utf-8', '{"exc_type": "FieldError", "exc_message": ["Invalid field name(s) given in select_related: \'id_contrato\'. Choices are: id_cliente, id_articulo"], "exc_module": "django.core.exceptions"}', '2026-03-24 00:51:04.318886', NULL, '{"children": []}', NULL, NULL, NULL, NULL, '2026-03-24 00:51:04.318824', NULL, NULL),
	(2, '9e84c8ef-aeb1-458c-87af-8134bdd3fd07', 'FAILURE', 'application/json', 'utf-8', '{"exc_type": "FieldError", "exc_message": ["Invalid field name(s) given in select_related: \'id_contrato\'. Choices are: id_cliente, id_articulo"], "exc_module": "django.core.exceptions"}', '2026-03-24 00:57:29.798082', NULL, '{"children": []}', NULL, NULL, NULL, NULL, '2026-03-24 00:57:29.798061', NULL, NULL),
	(3, '0c16883c-58de-48e0-9ae5-e357d77b5134', 'FAILURE', 'application/json', 'utf-8', '{"exc_type": "FieldError", "exc_message": ["Invalid field name(s) given in select_related: \'id_contrato\'. Choices are: id_cliente, id_articulo"], "exc_module": "django.core.exceptions"}', '2026-03-24 00:58:11.762655', NULL, '{"children": []}', NULL, NULL, NULL, NULL, '2026-03-24 00:58:11.762611', NULL, NULL),
	(4, '807f6705-f5c1-43ba-898d-c78e30121833', 'FAILURE', 'application/json', 'utf-8', '{"exc_type": "FieldError", "exc_message": ["Invalid field name(s) given in select_related: \'id_contrato\'. Choices are: id_cliente, id_articulo"], "exc_module": "django.core.exceptions"}', '2026-03-24 00:58:32.989770', NULL, '{"children": []}', NULL, NULL, NULL, NULL, '2026-03-24 00:58:32.989710', NULL, NULL),
	(5, '68f51392-7796-4f49-9a16-1d938f6f98e8', 'SUCCESS', 'application/json', 'utf-8', '"Cuotas generadas: 2026-03-24"', '2026-03-24 02:57:57.674260', NULL, '{"children": []}', NULL, NULL, NULL, NULL, '2026-03-24 02:57:57.674213', NULL, NULL),
	(6, '4a50643a-7183-4708-acb8-acdf755e4f57', 'SUCCESS', 'application/json', 'utf-8', '"Cuotas generadas: 2026-03-24"', '2026-03-24 22:35:39.204882', NULL, '{"children": []}', NULL, NULL, NULL, NULL, '2026-03-24 22:35:39.204839', NULL, NULL),
	(7, 'f111871e-4f17-4b1b-b2f0-936f9d9c923f', 'FAILURE', 'application/json', 'utf-8', '{"exc_type": "UnboundLocalError", "exc_message": ["cannot access local variable \'tipo\' where it is not associated with a value"], "exc_module": "builtins"}', '2026-03-24 22:41:51.303072', NULL, '{"children": []}', NULL, NULL, NULL, NULL, '2026-03-24 22:41:51.303043', NULL, NULL),
	(8, '9bd2ab00-dd12-43b6-bb8c-6a8aa3dceef6', 'FAILURE', 'application/json', 'utf-8', '{"exc_type": "UnboundLocalError", "exc_message": ["cannot access local variable \'tipo\' where it is not associated with a value"], "exc_module": "builtins"}', '2026-03-24 22:49:45.872981', NULL, '{"children": []}', NULL, NULL, NULL, NULL, '2026-03-24 22:49:45.872913', NULL, NULL),
	(9, '88b2e46c-240b-431e-b329-ea3c37b45b7e', 'FAILURE', 'application/json', 'utf-8', '{"exc_type": "AttributeError", "exc_message": ["\'Empeno\' object has no attribute \'id_contrato_id\'"], "exc_module": "builtins"}', '2026-03-24 22:50:32.795929', NULL, '{"children": []}', NULL, NULL, NULL, NULL, '2026-03-24 22:50:32.795898', NULL, NULL),
	(10, 'd44d76a1-000b-4523-9b7b-1f7f8a4d465f', 'SUCCESS', 'application/json', 'utf-8', '"Cuotas generadas: 2026-03-24"', '2026-03-24 22:53:40.233970', NULL, '{"children": []}', NULL, NULL, NULL, NULL, '2026-03-24 22:53:40.233932', NULL, NULL);

-- Volcando estructura para tabla diamante_azul.django_content_type
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.django_content_type: ~28 rows (aproximadamente)
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(1, 'admin', 'logentry'),
	(2, 'auth', 'permission'),
	(3, 'auth', 'group'),
	(4, 'auth', 'user'),
	(5, 'contenttypes', 'contenttype'),
	(6, 'sessions', 'session'),
	(7, 'articulos', 'articulos'),
	(8, 'clientes', 'cliente'),
	(9, 'empenos', 'cuota'),
	(10, 'empenos', 'pago'),
	(11, 'empenos', 'empeno'),
	(12, 'usuarios', 'rol'),
	(13, 'usuarios', 'usuario'),
	(14, 'factura', 'factura'),
	(15, 'factura', 'detallefactura'),
	(16, 'contratos', 'contrato'),
	(17, 'django_celery_beat', 'crontabschedule'),
	(18, 'django_celery_beat', 'intervalschedule'),
	(19, 'django_celery_beat', 'periodictask'),
	(20, 'django_celery_beat', 'periodictasks'),
	(21, 'django_celery_beat', 'solarschedule'),
	(22, 'django_celery_beat', 'clockedschedule'),
	(23, 'django_celery_results', 'taskresult'),
	(24, 'django_celery_results', 'chordcounter'),
	(25, 'django_celery_results', 'groupresult'),
	(26, 'compras', 'compra'),
	(27, 'notificaciones', 'notificacion'),
	(28, 'compras', 'ventaarticulo');

-- Volcando estructura para tabla diamante_azul.django_migrations
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.django_migrations: ~74 rows (aproximadamente)
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
	(1, 'contenttypes', '0001_initial', '2026-03-08 23:00:47.279959'),
	(2, 'auth', '0001_initial', '2026-03-08 23:00:47.780018'),
	(3, 'admin', '0001_initial', '2026-03-08 23:00:47.877376'),
	(4, 'admin', '0002_logentry_remove_auto_add', '2026-03-08 23:00:47.884510'),
	(5, 'admin', '0003_logentry_add_action_flag_choices', '2026-03-08 23:00:47.891148'),
	(6, 'articulos', '0001_initial', '2026-03-08 23:00:47.902833'),
	(7, 'contenttypes', '0002_remove_content_type_name', '2026-03-08 23:00:47.960041'),
	(8, 'auth', '0002_alter_permission_name_max_length', '2026-03-08 23:00:48.008339'),
	(9, 'auth', '0003_alter_user_email_max_length', '2026-03-08 23:00:48.021918'),
	(10, 'auth', '0004_alter_user_username_opts', '2026-03-08 23:00:48.029890'),
	(11, 'auth', '0005_alter_user_last_login_null', '2026-03-08 23:00:48.068106'),
	(12, 'auth', '0006_require_contenttypes_0002', '2026-03-08 23:00:48.070530'),
	(13, 'auth', '0007_alter_validators_add_error_messages', '2026-03-08 23:00:48.077968'),
	(14, 'auth', '0008_alter_user_username_max_length', '2026-03-08 23:00:48.090337'),
	(15, 'auth', '0009_alter_user_last_name_max_length', '2026-03-08 23:00:48.103490'),
	(16, 'auth', '0010_alter_group_name_max_length', '2026-03-08 23:00:48.117808'),
	(17, 'auth', '0011_update_proxy_permissions', '2026-03-08 23:00:48.124964'),
	(18, 'auth', '0012_alter_user_first_name_max_length', '2026-03-08 23:00:48.149782'),
	(19, 'clientes', '0001_initial', '2026-03-08 23:00:48.175398'),
	(20, 'usuarios', '0001_initial', '2026-03-08 23:00:48.264417'),
	(21, 'factura', '0001_initial', '2026-03-08 23:00:48.486160'),
	(22, 'empenos', '0001_initial', '2026-03-08 23:00:48.731105'),
	(23, 'contratos', '0001_initial', '2026-03-08 23:00:48.954353'),
	(24, 'contratos', '0002_initial', '2026-03-08 23:00:49.073443'),
	(25, 'sessions', '0001_initial', '2026-03-08 23:00:49.098641'),
	(26, 'clientes', '0002_cliente_id_usuario_alter_cliente_table', '2026-03-12 00:21:51.522725'),
	(27, 'articulos', '0002_alter_articulos_estado_alter_articulos_quilataje', '2026-03-18 15:59:13.293532'),
	(28, 'clientes', '0003_cliente_lugar_expedicion', '2026-03-21 18:27:03.901550'),
	(29, 'empenos', '0002_empeno_num_cuotas_alter_empeno_estado', '2026-03-21 18:37:22.090310'),
	(30, 'clientes', '0004_cliente_departamento_expedicion', '2026-03-22 18:50:43.422113'),
	(31, 'django_celery_beat', '0001_initial', '2026-03-24 00:22:34.428415'),
	(32, 'django_celery_beat', '0002_auto_20161118_0346', '2026-03-24 00:22:34.498871'),
	(33, 'django_celery_beat', '0003_auto_20161209_0049', '2026-03-24 00:22:34.515108'),
	(34, 'django_celery_beat', '0004_auto_20170221_0000', '2026-03-24 00:22:34.520897'),
	(35, 'django_celery_beat', '0005_add_solarschedule_events_choices', '2026-03-24 00:22:34.526568'),
	(36, 'django_celery_beat', '0006_auto_20180322_0932', '2026-03-24 00:22:34.573586'),
	(37, 'django_celery_beat', '0007_auto_20180521_0826', '2026-03-24 00:22:34.598569'),
	(38, 'django_celery_beat', '0008_auto_20180914_1922', '2026-03-24 00:22:34.644552'),
	(39, 'django_celery_beat', '0006_auto_20180210_1226', '2026-03-24 00:22:34.674625'),
	(40, 'django_celery_beat', '0006_periodictask_priority', '2026-03-24 00:22:34.689346'),
	(41, 'django_celery_beat', '0009_periodictask_headers', '2026-03-24 00:22:34.707859'),
	(42, 'django_celery_beat', '0010_auto_20190429_0326', '2026-03-24 00:22:34.893050'),
	(43, 'django_celery_beat', '0011_auto_20190508_0153', '2026-03-24 00:22:34.965125'),
	(44, 'django_celery_beat', '0012_periodictask_expire_seconds', '2026-03-24 00:22:34.981900'),
	(45, 'django_celery_beat', '0013_auto_20200609_0727', '2026-03-24 00:22:34.991054'),
	(46, 'django_celery_beat', '0014_remove_clockedschedule_enabled', '2026-03-24 00:22:35.002810'),
	(47, 'django_celery_beat', '0015_edit_solarschedule_events_choices', '2026-03-24 00:22:35.008782'),
	(48, 'django_celery_beat', '0016_alter_crontabschedule_timezone', '2026-03-24 00:22:35.017861'),
	(49, 'django_celery_beat', '0017_alter_crontabschedule_month_of_year', '2026-03-24 00:22:35.024710'),
	(50, 'django_celery_beat', '0018_improve_crontab_helptext', '2026-03-24 00:22:35.034547'),
	(51, 'django_celery_beat', '0019_alter_periodictasks_options', '2026-03-24 00:22:35.039015'),
	(52, 'django_celery_results', '0001_initial', '2026-03-24 00:22:35.072992'),
	(53, 'django_celery_results', '0002_add_task_name_args_kwargs', '2026-03-24 00:22:35.095187'),
	(54, 'django_celery_results', '0003_auto_20181106_1101', '2026-03-24 00:22:35.100816'),
	(55, 'django_celery_results', '0004_auto_20190516_0412', '2026-03-24 00:22:35.148086'),
	(56, 'django_celery_results', '0005_taskresult_worker', '2026-03-24 00:22:35.167602'),
	(57, 'django_celery_results', '0006_taskresult_date_created', '2026-03-24 00:22:35.210645'),
	(58, 'django_celery_results', '0007_remove_taskresult_hidden', '2026-03-24 00:22:35.222562'),
	(59, 'django_celery_results', '0008_chordcounter', '2026-03-24 00:22:35.251496'),
	(60, 'django_celery_results', '0009_groupresult', '2026-03-24 00:22:36.480567'),
	(61, 'django_celery_results', '0010_remove_duplicate_indices', '2026-03-24 00:22:36.488121'),
	(62, 'django_celery_results', '0011_taskresult_periodic_task_name', '2026-03-24 00:22:36.501732'),
	(63, 'django_celery_results', '0012_taskresult_date_started', '2026-03-24 00:22:36.515128'),
	(64, 'django_celery_results', '0013_taskresult_django_cele_periodi_1993cf_idx', '2026-03-24 00:22:36.530507'),
	(65, 'django_celery_results', '0014_alter_taskresult_status', '2026-03-24 00:22:36.536405'),
	(66, 'contratos', '0003_alter_contrato_tipo_contrato', '2026-03-24 00:52:49.551430'),
	(67, 'empenos', '0003_pago_id_contrato', '2026-03-24 00:52:49.638180'),
	(68, 'empenos', '0004_empeno_id_contrato_alter_empeno_num_cuotas', '2026-03-24 22:53:05.822560'),
	(69, 'compras', '0001_initial', '2026-03-25 23:50:10.882507'),
	(70, 'empenos', '0005_cuota_id_cliente', '2026-03-27 12:03:30.534541'),
	(71, 'notificaciones', '0001_initial', '2026-04-01 21:09:22.487988'),
	(72, 'compras', '0002_alter_compra_estado_ventaarticulo', '2026-04-06 21:07:24.950149'),
	(73, 'compras', '0003_remove_ventaarticulo_fecha_venta_and_more', '2026-04-07 00:13:32.804422'),
	(74, 'factura', '0002_alter_detallefactura_id_articulo', '2026-04-07 00:17:55.366021');

-- Volcando estructura para tabla diamante_azul.django_session
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.django_session: ~34 rows (aproximadamente)
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
	('09368bhijm4yfqj1p1m6g7d6a00sv141', '.eJyrViotLk0sysyPz0xRsrLUgXPz8nOTilKVrJQyMtPzlRDiRfk5SlZKzjmZqXklqajiYCOMawHfDR2G:1w29Rr:11IcfmHtjNd3FGGkJWtLmljLPcQ8M9MpDxT0vQRTDGY', '2026-03-17 15:01:39.336827'),
	('10nd0sv3tivahkzap3zk80xrwde88l5j', '.eJxVjkEOwiAQRe_CuiFAK2B3uvcMzcCMFm0hgXZlvLup1tgu57-Xl3myDuap7-ZCuQvIWqZYtd0c-AfFBeAd4i1xn-KUg-OLwlda-CUhDefV3QV6KP2SJSPM0WkSYK3yHrxVwl4bIYzxThFibUBTUx-UlY0TUiMq75VuyAogySo2lxlySJ835f-MaXSZWMtOOIa48XIafmsoUwZMeU-_pdcbsppXPA:1wG1pw:vruADhRfKmlVapFgi8O1miB2GHYuDScJt7Lw9s2s1SQ', '2026-04-24 21:43:52.104108'),
	('2k86bblzb80j5cwg3efnsti7q9zj0ldf', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJQcU3Iz85QQEkX5OTDRzOKSosSU_CJUWYhJtQC6oiBL:1wBBJF:rSKiz9Xyfu6zGhDCT18aOb1siaq5kDnxuEsgd3JhFUk', '2026-04-11 12:50:05.199331'),
	('2w75rgahcj1m1mbcsjxynva6fvgvxr3y', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJQcU3Iz85QQEkX5OTDRzOKSosSU_CJUWYhJtQC6oiBL:1wEzbt:FbKjtQzjetNKUtQrQUhCkDVmTDh9qElLzhuDqupOzQM', '2026-04-22 01:09:05.484570'),
	('30ug622r6x7skawper1fqfi32wv6we29', '.eJyrViotLk0sysyPz0xRsjI01oHz8_Jzk4pSlayUIktzMlNLMpQQUkX5OUpWSs45mal5Jamo4mBjjGsBU_ce7g:1w7MUV:Sl8w9DbU4KLbhsv1kj36QX9eREosnu162s8G_MloCmo', '2026-03-31 23:57:55.403500'),
	('5iqfc1lnmqfhxs5w2ioz47ne0a5f9utn', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJQcU3Iz85QQEkX5OTDRzOKSosSU_CJUWYhJtQC6oiBL:1w2Far:zRbwmEvUPgFvkbAG8l3utJ1szyNF2LUvLauk-Nrb5H0', '2026-03-17 21:35:21.153529'),
	('7t9houmw7nejv4bnonp1nydpji5yzjka', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJQcU3Iz85QQEkX5OTDRzOKSosSU_CJUWYhJtQC6oiBL:1w8ojP:SriL3l30lwDRfu5A5gAh3g1TpZYyMzjjzWOaMjLsgCc', '2026-04-05 00:19:19.721807'),
	('85fe7yeua3hc0ud8n9atg7uj62rnsj8p', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJQcU3Iz85QQEkX5OTDRzOKSosSU_CJUWYhJtQC6oiBL:1w9BH2:XSPeQDoUlW27meGtiprbIbYnhsRWbY8yp_lG048w1uk', '2026-04-06 00:23:32.632518'),
	('9z6yqqhncv8y5avhs347lzkt61x724c4', '.eJyrViotLk0sysyPz0xRsjLTgXPz8nOTilKVrJRKSnMy85UQEkX5OUpWSs45mal5Jamo4mAzjGsBBHoeCQ:1w26On:zsEJ6F9Dbp9jNuQjO7nE9BKpku1E5Mf3xjyrqMgmow4', '2026-03-17 11:46:17.168655'),
	('a79u4shesfcqfksokxq87f1hrrbclkvd', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJQcU3Iz85QQEkX5OTDRzOKSosSU_CJUWYhJtQC6oiBL:1w2AHT:Wzs0fyHAaFYV1yVpAcGb8OmHLuFjQy3_AnvNicbbvuY', '2026-03-17 15:54:59.143063'),
	('b3pm62ik78yxl26425xismry6yc9s7cd', '.eJyrViotLk0sysyPz0xRsjLRgXPz8nOTilKVrJQc81KKUosV3EsTKxOT8pUQKoryc5SslFxzC3JSE1PQJMCmGdUCAD5JIYE:1w26kO:ELTOIa3TGAYzd6hzR8aSRfE-AMXMj5uC7PCIrkGDDBI', '2026-03-17 12:08:36.843375'),
	('c87c2c7ac04u63ycws4v96o722cx1pg0', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJQcU3Iz85QQEkX5OTDRzOKSosSU_CJUWYhJtQC6oiBL:1wGi0T:6U-S_1JEm3wUYKRhO2B5ivNZdqtcSdA09JvR_PW2Ip4', '2026-04-26 18:45:33.458843'),
	('ctggdcqofzknz0g7tgs2l4c08vod55cw', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJQcU3Iz85QQEkX5OTDRzOKSosSU_CJUWYhJtQC6oiBL:1w5RRu:xBsi7bwQmJb6D84MSpF61s4NW1lExpXKQnWYZ_OersA', '2026-03-26 16:51:18.276012'),
	('dhnc25a2btnro3i1abeglzakvpawg0ia', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJQcU3Iz85QQEkX5OTDRzOKSosSU_CJUWYhJtQC6oiBL:1wFcd1:eBaMfKQtOWZHRy2PSi_02kCYNlf-Jc3_3ApfpUlo9NM', '2026-04-23 18:48:51.357807'),
	('dppcaskuizhseajfyp0bnigw1ix8af36', '.eJyrViotLk0sysyPz0xRsjK00IHz8_Jzk4pSlayUHPNSilKLFdxSczILUhXCEpOTE5UQyoryc5SslJxzMlPzSlJRxcFGGtcCANJPIt8:1wBAWW:tYvWU0KtADEPhvuKh5VFJy0qQfRHx0rdVkYIMG5qtZ4', '2026-04-11 11:59:44.893501'),
	('fnlk9pzoiv3xjtktzy6b0hywkt0r23ea', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJQcU3Iz85QQEkX5OTDRzOKSosSU_CJUWYhJtQC6oiBL:1wATos:v2yeCeDc449yGF3mZV0p15d4C47hWMi1qyZMpKdJuVU', '2026-04-09 14:23:50.815611'),
	('h6ooemoezcvtfauaxvha0t96rd1wd4rp', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJQcU3Iz85QQEkX5OTDRzOKSosSU_CJUWYhJtQC6oiBL:1wBggF:ppWVM3Ki07g-LrFu6EQigxhRMB8QPpre6LbffhnFR8w', '2026-04-12 22:19:55.094160'),
	('ia8mdm6f574q2zpj2qqm998lhhqki35u', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJQcU3Iz85QQEkX5OTDRzOKSosSU_CJUWYhJtQC6oiBL:1w1utd:bIYbeNnT5gqzQrFAKCwlSRqpLi4yqOu1_fuyhnYMpqI', '2026-03-16 23:29:21.191342'),
	('izjebctgklibwbye8lboow45llob1ji0', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJQcU3Iz85QQEkX5OTDRzOKSosSU_CJUWYhJtQC6oiBL:1wDNX5:Foh9AYqejTUIj22PcIaEneeiHXwZb9bPxo7O-_n-aMU', '2026-04-17 14:17:27.469735'),
	('jq1a4pfu3fnhonlvcvg7vw01xk8klcuc', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJQcU3Iz85QQEkX5OTDRzOKSosSU_CJUWYhJtQC6oiBL:1wCjMV:N8b7s1qiXsVKYHTRi9fsS4vBOqZnIxNVqxujnrPx-xQ', '2026-04-15 19:23:51.373234'),
	('jr8c7ta0tthajsp903na9n1qdhiy23hq', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJQcU3Iz85QQEkX5OTDRzOKSosSU_CJUWYhJtQC6oiBL:1w52UM:S9hoC18i8xkNKfB4gQMacZD-v7rtLxaY2uoVsHErB10', '2026-03-25 14:12:10.424304'),
	('kd4f2yi5oi1o0szmsbfwz9i0lmbjl75v', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJQcU3Iz85QQEkX5OTDRzOKSosSU_CJUWYhJtQC6oiBL:1w9qob:k9KC8fDDMJaC0TUanCTpzeKL2_mdR4-tvlKxQC9IA-8', '2026-04-07 20:44:57.655905'),
	('o1qy3nl289gc0gh17x3xz66e7fzm89eu', '.eJyrViotLk0sysyPz0xRsjLXgXPz8nOTilKVrJQySnOTUotK8pUQckX5OUpWSs45mal5Jamo4mBjjGsBaKUfQw:1w26fF:tjxZjlQ63dZqPRCPHKkvVygAYxV6LKCCYZDB8zhPvh4', '2026-03-17 12:03:17.345952'),
	('ojdb3n27tvfk5x22mqdsjziec4xwg4ix', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJQcU3Iz85QQEkX5OTDRzOKSosSU_CJUWYhJtQC6oiBL:1w67ES:nRWH4r3ySgnaiRbIWbV7as4bKvKPtyA8dtvfkS8rlrI', '2026-03-28 13:28:12.686169'),
	('or1wn5ibmas388h3h55zxqdn7143ubgo', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJQcU3Iz85QQEkX5OTDRzOKSosSU_CJUWYhJtQC6oiBL:1w4QOI:QjJvPqDXMEPQI246LX8wl4YdUPdyHGZIrE96b-ged6A', '2026-03-23 21:31:22.072625'),
	('p0gtb04i4dgu5e8hi2sedjbjyh1uvcfi', '.eJyrViotLk0sysyPz0xRsjLRgXPz8nOTilKVrJQc81KKUosV3EsTKxOT8pUQKoryc5SslJxzMlPzSlJRxcGGGdcCABv1IR8:1w5XMc:umPKQ04l4jLX0RHxXuJ_EI2v6sxWc8Tl3b4jET8djBg', '2026-03-26 23:10:14.150359'),
	('p45x5tl9x5s8kne0qtsokgm0wik272l9', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJQcU3Iz85QQEkX5OTDRzOKSosSU_CJUWYhJtQC6oiBL:1w7Hpd:mOlmTsQ7NNfdp29YG_2GCU7qNX9Bh4hICrfmtqAVnvk', '2026-03-31 18:59:25.358501'),
	('q9qcdhy5zivq772geq4s27zdm1opydlg', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJQcU3Iz85QQEkX5OTDRzOKSosSU_CJUWYhJtQC6oiBL:1w0VNv:Tm7P-oB0aQHBXRF0Rk9ctdHhqka8YJlXmhCTzCkDtkU', '2026-03-13 02:02:47.206399'),
	('rg8ndvgx43ngrpvxumo6i0z65y67w8dc', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJQcU3Iz85QQEkX5OTDRzOKSosSU_CJUWYhJtQC6oiBL:1w18d5:S-iBktaX3lVGLJpsdAxA7CCK0NA2mgtqOcC2B0sHQ2I', '2026-03-14 19:57:03.209213'),
	('sclmcynvquy1l803k4z2e45n7mpbmvtw', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJQcU3Iz85QQEkX5OTDRzOKSosSU_CJUWYhJtQC6oiBL:1w2omv:FtLxPHUzYB0vGZjtpEYJsUZYWBB2qHoA4lhh2aSU6pw', '2026-03-19 11:10:09.908167'),
	('t201e0qp02s9oyhaxudwv4diyt4qm2yg', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJQcU3Iz85QQEkX5OTDRzOKSosSU_CJUWYhJtQC6oiBL:1vzgwc:kZT_4VqrxHFag25UlaA-MNKFcstkm7jMHfqxtVzni-w', '2026-03-10 20:11:14.771509'),
	('wccmtcp45atf0f4w712j7sc2jvoiswxr', '.eJyrViotLk0sysyPz0xRsjI01oHz8_Jzk4pSlayUIktzMlNLMpQQUkX5OUpWSs45mal5Jamo4mBjjGsBU_ce7g:1w67TO:_rOGHKqeEcjATjjshNgwcLd41xuJIY9cpgys2GVaVTE', '2026-03-28 13:43:38.393513'),
	('xhucbf7qiyarol9kraqvj2aflc14kpyv', '.eJyrViotLk0sysyPz0xRsjLRgXPz8nOTilKVrJQc81KKUosV3EsTKxOT8pUQKoryc5SslFxzC3JSE1PQJMCmGdUCAD5JIYE:1w29QT:7InwFjJZg81e1v5371whNKGIPZ6PGwSae8h8URL3qwI', '2026-03-17 15:00:13.753245'),
	('xjzz1a5nxaojw25wbakmlz54n7tm7tsa', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJQcU3Iz85QQEkX5OTDRzOKSosSU_CJUWYhJtQC6oiBL:1w2pvo:5XU0g8r931Gv4QNcs65x5OSvYdNoFL-5i6RmHoZrYBo', '2026-03-19 12:23:24.477730'),
	('zwqez8seecsvqa6zwawxbn7qt30mm38u', '.eJyrViotLk0sysyPz0xRsjLUgXPz8nOTilKVrJQcU3Iz85QQEkX5OTDRzOKSosSU_CJUWYhJtQC6oiBL:1w7yos:3x4oXBNxHttEpCe7OqTvRjWv7nqIOLaxaA5EmfAuub8', '2026-04-02 16:53:30.734898');

-- Volcando estructura para tabla diamante_azul.empenos
CREATE TABLE IF NOT EXISTS `empenos` (
  `id_empeno` int(11) NOT NULL AUTO_INCREMENT,
  `monto_prestado` decimal(10,2) NOT NULL,
  `tasa_interes` decimal(5,2) NOT NULL,
  `fecha_inicio` datetime(6) NOT NULL,
  `fecha_vencimiento` date NOT NULL,
  `estado` enum('Activo','En venta','Vendido','Vencido') NOT NULL,
  `monto_entregado` decimal(10,2) NOT NULL,
  `fecha_entrega` datetime(6) NOT NULL,
  `id_articulo_id` int(11) NOT NULL,
  `id_cliente_id` int(11) NOT NULL,
  `num_cuotas` int(11) NOT NULL DEFAULT 1,
  `id_contrato_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_empeno`),
  KEY `empenos_id_articulo_id_1c43bb41_fk_articulos_id_articulo` (`id_articulo_id`),
  KEY `empenos_id_cliente_id_34865241_fk_clientes_cliente_id_cliente` (`id_cliente_id`),
  KEY `empenos_id_contrato_id_e85ed427_fk_contrato_id_contrato` (`id_contrato_id`),
  CONSTRAINT `empenos_id_articulo_id_1c43bb41_fk_articulos_id_articulo` FOREIGN KEY (`id_articulo_id`) REFERENCES `articulos` (`id_articulo`),
  CONSTRAINT `empenos_id_cliente_id_34865241_fk_clientes_cliente_id_cliente` FOREIGN KEY (`id_cliente_id`) REFERENCES `clientes` (`id_cliente`),
  CONSTRAINT `empenos_id_contrato_id_e85ed427_fk_contrato_id_contrato` FOREIGN KEY (`id_contrato_id`) REFERENCES `contrato` (`id_contrato`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.empenos: ~21 rows (aproximadamente)
INSERT INTO `empenos` (`id_empeno`, `monto_prestado`, `tasa_interes`, `fecha_inicio`, `fecha_vencimiento`, `estado`, `monto_entregado`, `fecha_entrega`, `id_articulo_id`, `id_cliente_id`, `num_cuotas`, `id_contrato_id`) VALUES
	(2, 50000.00, 10.00, '2026-03-13 23:56:10.464098', '2026-03-13', 'Vencido', 50000.00, '2026-03-13 23:56:10.464193', 2, 2, 1, 21),
	(3, 30000.00, 10.00, '2026-03-16 01:32:39.559214', '2026-03-16', 'Vencido', 30000.00, '2026-03-16 01:32:39.559259', 3, 2, 1, 1),
	(6, 130000.00, 10.00, '2026-03-16 16:00:22.780584', '2026-04-16', 'Vencido', 130000.00, '2026-03-16 16:00:22.780623', 4, 2, 1, 3),
	(7, 123344.00, 10.00, '2026-03-18 02:00:32.745437', '2026-04-17', 'Vencido', 123344.00, '2026-03-18 02:00:32.745534', 5, 8, 1, 4),
	(8, 1000000.00, 10.00, '2026-03-18 12:30:05.352949', '2026-04-18', 'Vencido', 1000000.00, '2026-03-18 12:30:05.353009', 8, 9, 1, 7),
	(9, 50000.00, 10.00, '2026-03-24 22:40:49.611180', '2026-04-24', 'Activo', 50000.00, '2026-03-24 22:40:49.611255', 9, 8, 1, NULL),
	(10, 50000.00, 10.00, '2026-03-27 13:33:39.898694', '2026-04-27', 'Activo', 50000.00, '2026-03-27 13:33:39.898732', 15, 11, 1, 5),
	(11, 130000.00, 10.00, '2026-03-27 13:36:29.687027', '2026-04-27', 'Activo', 130000.00, '2026-03-27 13:36:29.687102', 25, 11, 1, 8),
	(12, 12000.00, 10.00, '2026-04-01 19:49:11.396193', '2026-05-01', 'Activo', 12000.00, '2026-04-01 19:49:11.396410', 12, 9, 1, 6),
	(13, 213234.00, 10.00, '2026-04-02 16:28:45.939516', '2026-05-02', 'Activo', 213234.00, '2026-04-02 16:28:45.939566', 26, 4, 1, 9),
	(14, 500000.00, 10.00, '2026-04-08 19:15:59.387638', '2026-05-08', 'Activo', 500000.00, '2026-04-08 19:15:59.387682', 18, 13, 1, 10),
	(15, 300000.00, 10.00, '2026-04-08 19:42:59.751357', '2026-05-08', 'Activo', 300000.00, '2026-04-08 19:42:59.751394', 24, 13, 1, 12),
	(16, 103000.00, 10.00, '2026-04-10 12:37:51.197762', '2026-05-10', 'Activo', 123000.00, '2026-04-10 12:37:51.197802', 68, 18, 1, 19),
	(17, 10000000.00, 10.00, '2026-04-10 12:52:18.159006', '2026-07-10', 'Activo', 10000000.00, '2026-04-10 12:52:18.159050', 77, 18, 1, 20),
	(18, 190000.00, 10.00, '2026-04-12 02:37:55.805520', '2026-05-12', 'Activo', 190000.00, '2026-04-12 02:37:55.805634', 61, 17, 1, 18),
	(19, 1400000.00, 10.00, '2026-04-24 01:41:50.901765', '2026-05-23', 'Activo', 1400000.00, '2026-04-24 01:41:50.901803', 67, 15, 1, 23),
	(20, 100000.00, 10.00, '2026-04-24 01:42:50.393370', '2026-05-23', 'Activo', 100000.00, '2026-04-24 01:42:50.393404', 39, 12, 1, 25),
	(21, 12000000.00, 10.00, '2026-04-24 01:47:16.159843', '2026-04-23', 'Vencido', 12000000.00, '2026-04-24 01:47:16.159876', 77, 8, 1, 27),
	(22, 8000.00, 10.00, '2026-04-24 01:48:29.049549', '2026-05-23', 'Activo', 8000.00, '2026-04-24 01:48:29.049587', 78, 12, 1, 29),
	(23, 10000.00, 10.00, '2026-04-24 01:50:05.788916', '2026-05-23', 'Activo', 10000.00, '2026-04-24 01:50:05.788945', 79, 4, 1, 30),
	(24, 10000.00, 10.00, '2026-04-24 01:51:24.874023', '2026-05-23', 'Activo', 10000.00, '2026-04-24 01:51:24.874080', 79, 4, 1, 32),
	(25, 10000.00, 10.00, '2026-04-24 01:52:05.825407', '2026-05-23', 'Activo', 10000.00, '2026-04-24 01:52:05.825489', 79, 4, 1, 34);

-- Volcando estructura para tabla diamante_azul.facturas
CREATE TABLE IF NOT EXISTS `facturas` (
  `id_factura` int(11) NOT NULL AUTO_INCREMENT,
  `fecha_venta` datetime(6) NOT NULL,
  `total_neto` decimal(10,2) DEFAULT NULL,
  `monto_pagado` decimal(10,2) NOT NULL,
  `metodo_pago` varchar(15) NOT NULL,
  `id_cliente_id` int(11) NOT NULL,
  `id_usuario_id` int(11) NOT NULL,
  PRIMARY KEY (`id_factura`),
  KEY `facturas_id_cliente_id_47985417_fk_clientes_cliente_id_cliente` (`id_cliente_id`),
  KEY `facturas_id_usuario_id_78667895_fk_usuarios_usuario_id_usuario` (`id_usuario_id`),
  CONSTRAINT `facturas_id_cliente_id_47985417_fk_clientes_cliente_id_cliente` FOREIGN KEY (`id_cliente_id`) REFERENCES `clientes` (`id_cliente`),
  CONSTRAINT `facturas_id_usuario_id_78667895_fk_usuarios_usuario_id_usuario` FOREIGN KEY (`id_usuario_id`) REFERENCES `usuarios_usuario` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.facturas: ~16 rows (aproximadamente)
INSERT INTO `facturas` (`id_factura`, `fecha_venta`, `total_neto`, `monto_pagado`, `metodo_pago`, `id_cliente_id`, `id_usuario_id`) VALUES
	(2, '2026-03-26 00:08:27.405960', 1999999.00, 1999999.00, 'Efectivo', 4, 1),
	(3, '2026-03-27 12:08:24.730084', 1000000.00, 1000000.00, 'Efectivo', 9, 1),
	(4, '2026-03-27 12:08:36.381525', 1200000.00, 1200000.00, 'Efectivo', 4, 1),
	(5, '2026-03-27 12:08:44.496151', 1200000.00, 1200000.00, 'Efectivo', 4, 1),
	(6, '2026-03-27 12:09:07.692491', 12001000.00, 12001000.00, 'Efectivo', 4, 1),
	(7, '2026-03-27 12:09:22.476882', 2000000.00, 2000000.00, 'Efectivo', 9, 1),
	(8, '2026-03-27 12:09:26.972304', 2000000.00, 2000000.00, 'Efectivo', 4, 1),
	(9, '2026-03-27 12:10:36.083172', 100.00, 100.00, 'Transferencia', 2, 1),
	(10, '2026-03-27 12:10:43.071731', 200.00, 200.00, 'Transferencia', 4, 1),
	(11, '2026-03-27 12:12:03.327473', 200.00, 200.00, 'Efectivo', 4, 1),
	(12, '2026-04-04 01:06:15.223366', 1234567.00, 1234567.00, 'Efectivo', 10, 1),
	(13, '2026-04-04 01:06:39.026517', 200.00, 200.00, 'Efectivo', 11, 1),
	(14, '2026-04-04 01:11:50.226929', 123423.00, 123423.00, 'Efectivo', 10, 1),
	(19, '2026-04-07 00:18:00.006550', 123145.00, 123145.00, 'Efectivo', 2, 1),
	(20, '2026-04-07 00:18:55.861262', 12345678.00, 12345678.00, 'Efectivo', 8, 1),
	(21, '2026-04-07 00:19:00.197608', 200.00, 200.00, 'Efectivo', 14, 1);

-- Volcando estructura para tabla diamante_azul.kombu_message
CREATE TABLE IF NOT EXISTS `kombu_message` (
  `id` int(11) NOT NULL,
  `visible` tinyint(1) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `payload` text NOT NULL,
  `version` smallint(6) NOT NULL,
  `queue_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_kombu_message_queue` (`queue_id`),
  KEY `ix_kombu_message_timestamp` (`timestamp`),
  KEY `ix_kombu_message_visible` (`visible`),
  KEY `ix_kombu_message_timestamp_id` (`timestamp`,`id`),
  CONSTRAINT `FK_kombu_message_queue` FOREIGN KEY (`queue_id`) REFERENCES `kombu_queue` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.kombu_message: ~10 rows (aproximadamente)
INSERT INTO `kombu_message` (`id`, `visible`, `timestamp`, `payload`, `version`, `queue_id`) VALUES
	(1, 0, '2026-03-23 19:51:04', '{"body": "W1tdLCB7fSwgeyJjYWxsYmFja3MiOiBudWxsLCAiZXJyYmFja3MiOiBudWxsLCAiY2hhaW4iOiBudWxsLCAiY2hvcmQiOiBudWxsfV0=", "content-encoding": "utf-8", "content-type": "application/json", "headers": {"lang": "py", "task": "empenos.tasks.generar_cuotas_mensuales", "id": "26d30da1-32f1-4bde-a543-46aba886a7d5", "shadow": null, "eta": null, "expires": null, "group": null, "group_index": null, "retries": 0, "timelimit": [null, null], "root_id": "26d30da1-32f1-4bde-a543-46aba886a7d5", "parent_id": null, "argsrepr": "()", "kwargsrepr": "{}", "origin": "gen14176@USUARIO", "ignore_result": false, "replaced_task_nesting": 0, "stamped_headers": null, "stamps": {}}, "properties": {"correlation_id": "26d30da1-32f1-4bde-a543-46aba886a7d5", "reply_to": "81f92fa2-91ce-3f8f-8fb5-7d042b1e6b94", "delivery_mode": 2, "delivery_info": {"exchange": "", "routing_key": "celery"}, "priority": 0, "body_encoding": "base64", "delivery_tag": "e1f646d2-0144-4962-b017-3bdad0426df0"}}', 2, 1),
	(2, 0, '2026-03-23 19:57:29', '{"body": "W1tdLCB7fSwgeyJjYWxsYmFja3MiOiBudWxsLCAiZXJyYmFja3MiOiBudWxsLCAiY2hhaW4iOiBudWxsLCAiY2hvcmQiOiBudWxsfV0=", "content-encoding": "utf-8", "content-type": "application/json", "headers": {"lang": "py", "task": "empenos.tasks.generar_cuotas_mensuales", "id": "9e84c8ef-aeb1-458c-87af-8134bdd3fd07", "shadow": null, "eta": null, "expires": null, "group": null, "group_index": null, "retries": 0, "timelimit": [null, null], "root_id": "9e84c8ef-aeb1-458c-87af-8134bdd3fd07", "parent_id": null, "argsrepr": "()", "kwargsrepr": "{}", "origin": "gen14176@USUARIO", "ignore_result": false, "replaced_task_nesting": 0, "stamped_headers": null, "stamps": {}}, "properties": {"correlation_id": "9e84c8ef-aeb1-458c-87af-8134bdd3fd07", "reply_to": "81f92fa2-91ce-3f8f-8fb5-7d042b1e6b94", "delivery_mode": 2, "delivery_info": {"exchange": "", "routing_key": "celery"}, "priority": 0, "body_encoding": "base64", "delivery_tag": "df68a9b7-45cd-4141-b8aa-97ee5bcf9b57"}}', 2, 1),
	(3, 0, '2026-03-23 19:58:11', '{"body": "W1tdLCB7fSwgeyJjYWxsYmFja3MiOiBudWxsLCAiZXJyYmFja3MiOiBudWxsLCAiY2hhaW4iOiBudWxsLCAiY2hvcmQiOiBudWxsfV0=", "content-encoding": "utf-8", "content-type": "application/json", "headers": {"lang": "py", "task": "empenos.tasks.generar_cuotas_mensuales", "id": "0c16883c-58de-48e0-9ae5-e357d77b5134", "shadow": null, "eta": null, "expires": null, "group": null, "group_index": null, "retries": 0, "timelimit": [null, null], "root_id": "0c16883c-58de-48e0-9ae5-e357d77b5134", "parent_id": null, "argsrepr": "()", "kwargsrepr": "{}", "origin": "gen14176@USUARIO", "ignore_result": false, "replaced_task_nesting": 0, "stamped_headers": null, "stamps": {}}, "properties": {"correlation_id": "0c16883c-58de-48e0-9ae5-e357d77b5134", "reply_to": "81f92fa2-91ce-3f8f-8fb5-7d042b1e6b94", "delivery_mode": 2, "delivery_info": {"exchange": "", "routing_key": "celery"}, "priority": 0, "body_encoding": "base64", "delivery_tag": "f1329a84-6c30-4e2e-984e-9a95ce149e5b"}}', 2, 1),
	(4, 0, '2026-03-23 19:58:32', '{"body": "W1tdLCB7fSwgeyJjYWxsYmFja3MiOiBudWxsLCAiZXJyYmFja3MiOiBudWxsLCAiY2hhaW4iOiBudWxsLCAiY2hvcmQiOiBudWxsfV0=", "content-encoding": "utf-8", "content-type": "application/json", "headers": {"lang": "py", "task": "empenos.tasks.generar_cuotas_mensuales", "id": "807f6705-f5c1-43ba-898d-c78e30121833", "shadow": null, "eta": null, "expires": null, "group": null, "group_index": null, "retries": 0, "timelimit": [null, null], "root_id": "807f6705-f5c1-43ba-898d-c78e30121833", "parent_id": null, "argsrepr": "()", "kwargsrepr": "{}", "origin": "gen14176@USUARIO", "ignore_result": false, "replaced_task_nesting": 0, "stamped_headers": null, "stamps": {}}, "properties": {"correlation_id": "807f6705-f5c1-43ba-898d-c78e30121833", "reply_to": "81f92fa2-91ce-3f8f-8fb5-7d042b1e6b94", "delivery_mode": 2, "delivery_info": {"exchange": "", "routing_key": "celery"}, "priority": 0, "body_encoding": "base64", "delivery_tag": "779e3e5a-88dc-4915-a82e-c09d9be9e7cb"}}', 2, 1),
	(5, 0, '2026-03-23 21:57:57', '{"body": "W1tdLCB7fSwgeyJjYWxsYmFja3MiOiBudWxsLCAiZXJyYmFja3MiOiBudWxsLCAiY2hhaW4iOiBudWxsLCAiY2hvcmQiOiBudWxsfV0=", "content-encoding": "utf-8", "content-type": "application/json", "headers": {"lang": "py", "task": "empenos.tasks.generar_cuotas_mensuales", "id": "68f51392-7796-4f49-9a16-1d938f6f98e8", "shadow": null, "eta": null, "expires": null, "group": null, "group_index": null, "retries": 0, "timelimit": [null, null], "root_id": "68f51392-7796-4f49-9a16-1d938f6f98e8", "parent_id": null, "argsrepr": "()", "kwargsrepr": "{}", "origin": "gen14176@USUARIO", "ignore_result": false, "replaced_task_nesting": 0, "stamped_headers": null, "stamps": {}}, "properties": {"correlation_id": "68f51392-7796-4f49-9a16-1d938f6f98e8", "reply_to": "81f92fa2-91ce-3f8f-8fb5-7d042b1e6b94", "delivery_mode": 2, "delivery_info": {"exchange": "", "routing_key": "celery"}, "priority": 0, "body_encoding": "base64", "delivery_tag": "08706fb1-65fa-45ea-b145-23362bb74a99"}}', 2, 1),
	(1001, 0, '2026-03-24 17:35:39', '{"body": "W1tdLCB7fSwgeyJjYWxsYmFja3MiOiBudWxsLCAiZXJyYmFja3MiOiBudWxsLCAiY2hhaW4iOiBudWxsLCAiY2hvcmQiOiBudWxsfV0=", "content-encoding": "utf-8", "content-type": "application/json", "headers": {"lang": "py", "task": "empenos.tasks.generar_cuotas_mensuales", "id": "4a50643a-7183-4708-acb8-acdf755e4f57", "shadow": null, "eta": null, "expires": null, "group": null, "group_index": null, "retries": 0, "timelimit": [null, null], "root_id": "4a50643a-7183-4708-acb8-acdf755e4f57", "parent_id": null, "argsrepr": "()", "kwargsrepr": "{}", "origin": "gen5544@USUARIO", "ignore_result": false, "replaced_task_nesting": 0, "stamped_headers": null, "stamps": {}}, "properties": {"correlation_id": "4a50643a-7183-4708-acb8-acdf755e4f57", "reply_to": "e73adae1-5ed1-30ae-8edb-4e4f99e5c04a", "delivery_mode": 2, "delivery_info": {"exchange": "", "routing_key": "celery"}, "priority": 0, "body_encoding": "base64", "delivery_tag": "cd10add9-3b0f-46e9-9a6f-78c83f96bed0"}}', 2, 1),
	(1002, 0, '2026-03-24 17:41:51', '{"body": "W1tdLCB7fSwgeyJjYWxsYmFja3MiOiBudWxsLCAiZXJyYmFja3MiOiBudWxsLCAiY2hhaW4iOiBudWxsLCAiY2hvcmQiOiBudWxsfV0=", "content-encoding": "utf-8", "content-type": "application/json", "headers": {"lang": "py", "task": "empenos.tasks.generar_cuotas_mensuales", "id": "f111871e-4f17-4b1b-b2f0-936f9d9c923f", "shadow": null, "eta": null, "expires": null, "group": null, "group_index": null, "retries": 0, "timelimit": [null, null], "root_id": "f111871e-4f17-4b1b-b2f0-936f9d9c923f", "parent_id": null, "argsrepr": "()", "kwargsrepr": "{}", "origin": "gen5544@USUARIO", "ignore_result": false, "replaced_task_nesting": 0, "stamped_headers": null, "stamps": {}}, "properties": {"correlation_id": "f111871e-4f17-4b1b-b2f0-936f9d9c923f", "reply_to": "e73adae1-5ed1-30ae-8edb-4e4f99e5c04a", "delivery_mode": 2, "delivery_info": {"exchange": "", "routing_key": "celery"}, "priority": 0, "body_encoding": "base64", "delivery_tag": "041619dd-e413-423e-b1ae-67a85c842370"}}', 2, 1),
	(1003, 0, '2026-03-24 17:49:45', '{"body": "W1tdLCB7fSwgeyJjYWxsYmFja3MiOiBudWxsLCAiZXJyYmFja3MiOiBudWxsLCAiY2hhaW4iOiBudWxsLCAiY2hvcmQiOiBudWxsfV0=", "content-encoding": "utf-8", "content-type": "application/json", "headers": {"lang": "py", "task": "empenos.tasks.generar_cuotas_mensuales", "id": "9bd2ab00-dd12-43b6-bb8c-6a8aa3dceef6", "shadow": null, "eta": null, "expires": null, "group": null, "group_index": null, "retries": 0, "timelimit": [null, null], "root_id": "9bd2ab00-dd12-43b6-bb8c-6a8aa3dceef6", "parent_id": null, "argsrepr": "()", "kwargsrepr": "{}", "origin": "gen5544@USUARIO", "ignore_result": false, "replaced_task_nesting": 0, "stamped_headers": null, "stamps": {}}, "properties": {"correlation_id": "9bd2ab00-dd12-43b6-bb8c-6a8aa3dceef6", "reply_to": "e73adae1-5ed1-30ae-8edb-4e4f99e5c04a", "delivery_mode": 2, "delivery_info": {"exchange": "", "routing_key": "celery"}, "priority": 0, "body_encoding": "base64", "delivery_tag": "5118c303-ede5-48e4-b618-010714bf43c9"}}', 2, 1),
	(1004, 0, '2026-03-24 17:50:32', '{"body": "W1tdLCB7fSwgeyJjYWxsYmFja3MiOiBudWxsLCAiZXJyYmFja3MiOiBudWxsLCAiY2hhaW4iOiBudWxsLCAiY2hvcmQiOiBudWxsfV0=", "content-encoding": "utf-8", "content-type": "application/json", "headers": {"lang": "py", "task": "empenos.tasks.generar_cuotas_mensuales", "id": "88b2e46c-240b-431e-b329-ea3c37b45b7e", "shadow": null, "eta": null, "expires": null, "group": null, "group_index": null, "retries": 0, "timelimit": [null, null], "root_id": "88b2e46c-240b-431e-b329-ea3c37b45b7e", "parent_id": null, "argsrepr": "()", "kwargsrepr": "{}", "origin": "gen5544@USUARIO", "ignore_result": false, "replaced_task_nesting": 0, "stamped_headers": null, "stamps": {}}, "properties": {"correlation_id": "88b2e46c-240b-431e-b329-ea3c37b45b7e", "reply_to": "e73adae1-5ed1-30ae-8edb-4e4f99e5c04a", "delivery_mode": 2, "delivery_info": {"exchange": "", "routing_key": "celery"}, "priority": 0, "body_encoding": "base64", "delivery_tag": "db98c655-6e24-4f71-bb11-9ce00a94990b"}}', 2, 1),
	(1005, 0, '2026-03-24 17:53:40', '{"body": "W1tdLCB7fSwgeyJjYWxsYmFja3MiOiBudWxsLCAiZXJyYmFja3MiOiBudWxsLCAiY2hhaW4iOiBudWxsLCAiY2hvcmQiOiBudWxsfV0=", "content-encoding": "utf-8", "content-type": "application/json", "headers": {"lang": "py", "task": "empenos.tasks.generar_cuotas_mensuales", "id": "d44d76a1-000b-4523-9b7b-1f7f8a4d465f", "shadow": null, "eta": null, "expires": null, "group": null, "group_index": null, "retries": 0, "timelimit": [null, null], "root_id": "d44d76a1-000b-4523-9b7b-1f7f8a4d465f", "parent_id": null, "argsrepr": "()", "kwargsrepr": "{}", "origin": "gen5544@USUARIO", "ignore_result": false, "replaced_task_nesting": 0, "stamped_headers": null, "stamps": {}}, "properties": {"correlation_id": "d44d76a1-000b-4523-9b7b-1f7f8a4d465f", "reply_to": "e73adae1-5ed1-30ae-8edb-4e4f99e5c04a", "delivery_mode": 2, "delivery_info": {"exchange": "", "routing_key": "celery"}, "priority": 0, "body_encoding": "base64", "delivery_tag": "59223e5d-a1c1-4b72-9f85-b1b05993a918"}}', 2, 1);

-- Volcando estructura para tabla diamante_azul.kombu_queue
CREATE TABLE IF NOT EXISTS `kombu_queue` (
  `id` int(11) NOT NULL,
  `name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.kombu_queue: ~1 rows (aproximadamente)
INSERT INTO `kombu_queue` (`id`, `name`) VALUES
	(1, 'celery');

-- Volcando estructura para tabla diamante_azul.message_id_sequence
CREATE TABLE IF NOT EXISTS `message_id_sequence` (
  `next_not_cached_value` bigint(21) NOT NULL,
  `minimum_value` bigint(21) NOT NULL,
  `maximum_value` bigint(21) NOT NULL,
  `start_value` bigint(21) NOT NULL COMMENT 'start value when sequences is created or value if RESTART is used',
  `increment` bigint(21) NOT NULL COMMENT 'increment value',
  `cache_size` bigint(21) unsigned NOT NULL,
  `cycle_option` tinyint(1) unsigned NOT NULL COMMENT '0 if no cycles are allowed, 1 if the sequence should begin a new cycle when maximum_value is passed',
  `cycle_count` bigint(21) NOT NULL COMMENT 'How many cycles have been done'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.message_id_sequence: ~0 rows (aproximadamente)
INSERT INTO `message_id_sequence` (`next_not_cached_value`, `minimum_value`, `maximum_value`, `start_value`, `increment`, `cache_size`, `cycle_option`, `cycle_count`) VALUES
	(2001, 1, 9223372036854775806, 1, 1, 1000, 0, 0);

-- Volcando estructura para tabla diamante_azul.notificaciones
CREATE TABLE IF NOT EXISTS `notificaciones` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `titulo` varchar(200) NOT NULL,
  `mensaje` longtext NOT NULL,
  `tipo` varchar(10) NOT NULL,
  `leida` tinyint(1) NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `url` varchar(300) DEFAULT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.notificaciones: ~65 rows (aproximadamente)
INSERT INTO `notificaciones` (`id`, `titulo`, `mensaje`, `tipo`, `leida`, `fecha`, `url`, `usuario_id`) VALUES
	(1, 'Nuevo cliente registrado', 'bueno (Doc: 242344234) fue registrado.', 'info', 0, '2026-04-01 21:20:20.998659', '/clientes/', NULL),
	(2, 'Contrato #8 creado', 'Tipo: Plazo Maximo. Cliente: jhjyjjjjjj.', 'success', 0, '2026-04-02 16:08:02.801589', '/contratos/detalle/8/', NULL),
	(3, 'Empeño #13 creado', 'Cliente: tulio. Monto: $213234.', 'success', 0, '2026-04-02 16:28:45.944325', '/empenos/detalle/13/', NULL),
	(4, 'Contrato #9 creado', 'Tipo: Plazo Maximo. Cliente: tulio.', 'success', 0, '2026-04-02 16:29:24.788559', '/contratos/detalle/9/', NULL),
	(5, 'Cuota pagada — Empeño #12', 'Cuota #1 pagada. Capital: $12000.00 + Interés: $1200.00.', 'success', 0, '2026-04-02 16:29:44.572357', '/empenos/detalle/12/', NULL),
	(6, 'Cuota pagada — Empeño #13', 'Cuota #1 pagada. Capital: $213234.00 + Interés: $21323.40.', 'success', 0, '2026-04-02 16:29:47.601920', '/empenos/detalle/13/', NULL),
	(7, 'Factura #12 generada', 'Cliente: nicolas. Total: $1234567.', 'info', 0, '2026-04-04 01:06:15.232769', '/factura/detalle/12/', NULL),
	(8, 'Factura #13 generada', 'Cliente: jhjyjjjjjj. Total: $200.00.', 'info', 0, '2026-04-04 01:06:39.030820', '/factura/detalle/13/', NULL),
	(9, 'Factura #14 generada', 'Cliente: nicolas. Total: $123423.', 'info', 0, '2026-04-04 01:11:50.230767', '/factura/detalle/14/', NULL),
	(10, 'Nuevo cliente registrado', 'Andres Felipe Vacca (Doc: 5734386) fue registrado.', 'info', 0, '2026-04-04 23:08:51.323534', '/clientes/', NULL),
	(11, 'Nuevo cliente registrado', 'FDSFDSFSF (Doc: 564563456) fue registrado.', 'info', 0, '2026-04-04 23:11:52.238608', '/clientes/', NULL),
	(16, 'Factura #19 generada', 'Cliente: Andres Guayabo. Total: $123145.00.', 'info', 0, '2026-04-07 00:18:00.009440', '/factura/detalle/19/', NULL),
	(17, 'Factura #20 generada', 'Cliente: aaaaaaaaaaa. Total: $12345678.00.', 'info', 0, '2026-04-07 00:18:55.863260', '/factura/detalle/20/', NULL),
	(18, 'Factura #21 generada', 'Cliente: FDSFDSFSF. Total: $200.00.', 'info', 0, '2026-04-07 00:19:00.199454', '/factura/detalle/21/', NULL),
	(19, 'Empeño #14 creado', 'Cliente: Andres Felipe Vacca. Monto: $500000.', 'success', 0, '2026-04-08 19:15:59.390323', '/empenos/detalle/14/', NULL),
	(20, 'Contrato #10 creado', 'Tipo: Normal. Cliente: Andres Felipe Vacca.', 'success', 0, '2026-04-08 19:16:26.431805', '/contratos/detalle/10/', NULL),
	(21, 'Empeño #15 creado', 'Cliente: Andres Felipe Vacca. Monto: $300000.', 'success', 0, '2026-04-08 19:42:59.756812', '/empenos/detalle/15/', NULL),
	(22, 'Contrato #11 creado', 'Tipo: Normal. Cliente: Andres Felipe Vacca.', 'success', 0, '2026-04-08 19:42:59.761400', '/contratos/detalle/11/', NULL),
	(23, 'Contrato #12 creado', 'Tipo: Normal   . Cliente: Andres Felipe Vacca.', 'success', 0, '2026-04-08 19:42:59.771248', '/contratos/detalle/12/', NULL),
	(24, 'Cuota pagada — Empeño #14', 'Cuota #1 pagada. Capital: $500000.00 + Interés: $50000.00.', 'success', 0, '2026-04-09 16:03:57.801805', '/empenos/detalle/14/', NULL),
	(25, 'Cuota pagada — Empeño #15', 'Cuota #1 pagada. Capital: $300000.00 + Interés: $30000.00.', 'success', 0, '2026-04-09 16:09:33.219629', '/empenos/detalle/15/', NULL),
	(26, 'Nuevo cliente registrado', 'pruebaNoti (Doc: 1132456786) fue registrado.', 'info', 0, '2026-04-09 20:13:01.550076', '/clientes/', NULL),
	(27, 'Nuevo cliente registrado', 'prueba2 (Doc: 132123123) fue registrado.', 'info', 0, '2026-04-09 20:15:11.924301', '/clientes/', NULL),
	(28, 'Nuevo cliente registrado', '[TEST] (Doc: 123456878) fue registrado.', 'info', 0, '2026-04-10 11:57:50.775330', '/clientes/', NULL),
	(29, 'Nuevo cliente registrado', 'Javier (Doc: 99999999) fue registrado.', 'info', 0, '2026-04-10 12:33:57.488977', '/clientes/', NULL),
	(30, 'Empeño #16 creado', 'Cliente: Javier. Monto: $123000.', 'success', 0, '2026-04-10 12:37:51.201622', '/empenos/detalle/16/', NULL),
	(31, 'Contrato #13 creado', 'Tipo: Normal. Cliente: Javier.', 'success', 0, '2026-04-10 12:37:51.207680', '/contratos/detalle/13/', NULL),
	(32, 'Contrato #14 creado', 'Tipo: Normal. Cliente: Javier.', 'success', 0, '2026-04-10 12:37:51.215834', '/contratos/detalle/14/', NULL),
	(33, 'Empeño #17 creado', 'Cliente: Javier. Monto: $10000000.', 'success', 0, '2026-04-10 12:52:18.161835', '/empenos/detalle/17/', NULL),
	(34, 'Contrato #15 creado', 'Tipo: Normal. Cliente: Javier.', 'success', 0, '2026-04-10 12:52:18.165253', '/contratos/detalle/15/', NULL),
	(35, 'Contrato #16 creado', 'Tipo: Normal. Cliente: Javier.', 'success', 0, '2026-04-10 12:52:18.172520', '/contratos/detalle/16/', NULL),
	(36, 'Cuota pagada — Empeño #17', 'Cuota #1 pagada. Capital: $10000000.00 + Interés: $1000000.00.', 'success', 0, '2026-04-12 02:17:33.053358', '/empenos/detalle/17/', NULL),
	(37, 'Cuota pagada — Empeño #16', 'Cuota #1 pagada. Capital: $123000.00 + Interés: $12300.00.', 'success', 0, '2026-04-12 02:20:17.650721', '/empenos/detalle/16/', NULL),
	(38, 'Empeño #18 creado', 'Cliente: [TEST]. Monto: $190000.', 'success', 0, '2026-04-12 02:37:55.808808', '/empenos/detalle/18/', NULL),
	(39, 'Contrato #17 creado', 'Tipo: Normal. Cliente: [TEST].', 'success', 0, '2026-04-12 02:37:55.814880', '/contratos/detalle/17/', NULL),
	(40, 'Contrato #18 creado', 'Tipo: Normal. Cliente: [TEST].', 'success', 0, '2026-04-12 02:37:55.823788', '/contratos/detalle/18/', NULL),
	(41, 'Contrato #19 creado', 'Tipo: Normal. Cliente: Javier.', 'success', 0, '2026-04-16 14:24:59.532716', '/contratos/detalle/19/', NULL),
	(42, 'Empeño #6 vencido', 'El empeño de Andres Guayabo ha vencido.', 'warning', 0, '2026-04-17 00:13:36.930766', '/empenos/detalle/6/', NULL),
	(43, 'Contrato #20 creado', 'Tipo: Normal. Cliente: Javier.', 'success', 0, '2026-04-17 01:24:12.605427', '/contratos/detalle/20/', NULL),
	(44, 'Empeño #7 vencido', 'El empeño de aaaaaaaaaaa ha vencido.', 'warning', 0, '2026-04-21 01:15:24.960304', '/empenos/detalle/7/', NULL),
	(45, 'Empeño #8 vencido', 'El empeño de Yulieth ha vencido.', 'warning', 0, '2026-04-21 01:15:24.968954', '/empenos/detalle/8/', NULL),
	(46, 'Cuota pagada — Empeño #18', 'Cuota #1 pagada. Capital: $0.00 + Interés: $19000.00.', 'success', 0, '2026-04-23 21:47:55.642650', '/empenos/detalle/18/', NULL),
	(47, 'Empeño #3 vencido', 'El empeño de Andres Guayabo ha vencido.', 'warning', 0, '2026-04-24 00:07:17.804920', '/empenos/detalle/3/', NULL),
	(48, 'Empeño #8 vencido', 'El empeño de Yulieth ha vencido.', 'warning', 0, '2026-04-24 00:08:01.150741', '/empenos/detalle/8/', NULL),
	(49, 'Contrato #21 creado', 'Tipo: Normal. Cliente: Andres Guayabo.', 'success', 0, '2026-04-24 00:08:04.410440', '/contratos/detalle/21/', NULL),
	(50, 'Empeño #2 vencido', 'El empeño de Andres Guayabo ha vencido.', 'warning', 0, '2026-04-24 00:08:04.424443', '/empenos/detalle/2/', NULL),
	(51, 'Empeño #19 creado', 'Cliente: pruebaNoti. Monto: $1400000.', 'success', 0, '2026-04-24 01:41:50.903254', '/empenos/detalle/19/', NULL),
	(52, 'Contrato #22 creado', 'Tipo: Normal. Cliente: pruebaNoti.', 'success', 0, '2026-04-24 01:41:50.905569', '/contratos/detalle/22/', NULL),
	(53, 'Contrato #23 creado', 'Tipo: Plazo Maximo. Cliente: pruebaNoti.', 'success', 0, '2026-04-24 01:41:50.908853', '/contratos/detalle/23/', NULL),
	(54, 'Empeño #20 creado', 'Cliente: bueno. Monto: $100000.', 'success', 0, '2026-04-24 01:42:50.394959', '/empenos/detalle/20/', NULL),
	(55, 'Contrato #24 creado', 'Tipo: Normal. Cliente: bueno.', 'success', 0, '2026-04-24 01:42:50.397688', '/contratos/detalle/24/', NULL),
	(56, 'Contrato #25 creado', 'Tipo: Contrato sobre Oro. Cliente: bueno.', 'success', 0, '2026-04-24 01:42:50.401309', '/contratos/detalle/25/', NULL),
	(57, 'Empeño #21 creado', 'Cliente: aaaaaaaaaaa. Monto: $12000000.', 'success', 0, '2026-04-24 01:47:16.161313', '/empenos/detalle/21/', NULL),
	(58, 'Contrato #26 creado', 'Tipo: Normal. Cliente: aaaaaaaaaaa.', 'success', 0, '2026-04-24 01:47:16.164028', '/contratos/detalle/26/', NULL),
	(59, 'Contrato #27 creado', 'Tipo: Plazo Maximo. Cliente: aaaaaaaaaaa.', 'success', 0, '2026-04-24 01:47:16.167563', '/contratos/detalle/27/', NULL),
	(60, 'Empeño #21 vencido', 'El empeño de aaaaaaaaaaa ha vencido.', 'warning', 0, '2026-04-24 01:47:16.182213', '/empenos/detalle/21/', NULL),
	(61, 'Empeño #22 creado', 'Cliente: bueno. Monto: $8000.', 'success', 0, '2026-04-24 01:48:29.051159', '/empenos/detalle/22/', NULL),
	(62, 'Contrato #28 creado', 'Tipo: Normal. Cliente: bueno.', 'success', 0, '2026-04-24 01:48:29.053798', '/contratos/detalle/28/', NULL),
	(63, 'Contrato #29 creado', 'Tipo: Plazo Maximo. Cliente: bueno.', 'success', 0, '2026-04-24 01:48:29.056939', '/contratos/detalle/29/', NULL),
	(64, 'Empeño #23 creado', 'Cliente: tulio. Monto: $10000.', 'success', 0, '2026-04-24 01:50:05.790302', '/empenos/detalle/23/', NULL),
	(65, 'Contrato #30 creado', 'Tipo: Normal. Cliente: tulio.', 'success', 0, '2026-04-24 01:50:05.792568', '/contratos/detalle/30/', NULL),
	(66, 'Contrato #31 creado', 'Tipo: Plazo Maximo. Cliente: tulio.', 'success', 0, '2026-04-24 01:50:05.796074', '/contratos/detalle/31/', NULL),
	(67, 'Empeño #24 creado', 'Cliente: tulio. Monto: $10000.', 'success', 0, '2026-04-24 01:51:24.875986', '/empenos/detalle/24/', NULL),
	(68, 'Contrato #32 creado', 'Tipo: Normal. Cliente: tulio.', 'success', 0, '2026-04-24 01:51:24.879123', '/contratos/detalle/32/', NULL),
	(69, 'Contrato #33 creado', 'Tipo: Plazo Maximo. Cliente: tulio.', 'success', 0, '2026-04-24 01:51:24.883609', '/contratos/detalle/33/', NULL),
	(70, 'Empeño #25 creado', 'Cliente: tulio. Monto: $10000.', 'success', 0, '2026-04-24 01:52:05.828163', '/empenos/detalle/25/', NULL),
	(71, 'Contrato #34 creado', 'Tipo: Normal. Cliente: tulio.', 'success', 0, '2026-04-24 01:52:05.833097', '/contratos/detalle/34/', NULL),
	(72, 'Contrato #35 creado', 'Tipo: Plazo Maximo. Cliente: tulio.', 'success', 0, '2026-04-24 01:52:05.838922', '/contratos/detalle/35/', NULL);

-- Volcando estructura para tabla diamante_azul.pagos
CREATE TABLE IF NOT EXISTS `pagos` (
  `id_pago` int(11) NOT NULL AUTO_INCREMENT,
  `fecha_pago` datetime(6) NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `metodo_pago` varchar(15) NOT NULL,
  `id_cliente_id` int(11) NOT NULL,
  `id_cuota_id` int(11) NOT NULL,
  `id_contrato_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_pago`),
  KEY `pagos_id_cliente_id_29fba4d2_fk_clientes_cliente_id_cliente` (`id_cliente_id`),
  KEY `pagos_id_cuota_id_f15ab543_fk_cuotas_id_cuota` (`id_cuota_id`),
  KEY `pagos_id_contrato_id_f4a0b16c_fk_contrato_id_contrato` (`id_contrato_id`),
  CONSTRAINT `pagos_id_cliente_id_29fba4d2_fk_clientes_cliente_id_cliente` FOREIGN KEY (`id_cliente_id`) REFERENCES `clientes` (`id_cliente`),
  CONSTRAINT `pagos_id_contrato_id_f4a0b16c_fk_contrato_id_contrato` FOREIGN KEY (`id_contrato_id`) REFERENCES `contrato` (`id_contrato`),
  CONSTRAINT `pagos_id_cuota_id_f15ab543_fk_cuotas_id_cuota` FOREIGN KEY (`id_cuota_id`) REFERENCES `cuotas` (`id_cuota`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.pagos: ~28 rows (aproximadamente)
INSERT INTO `pagos` (`id_pago`, `fecha_pago`, `monto`, `metodo_pago`, `id_cliente_id`, `id_cuota_id`, `id_contrato_id`) VALUES
	(1, '2026-03-18 15:25:28.300430', 55000.00, 'Efectivo', 2, 1, NULL),
	(2, '2026-03-18 15:26:20.982075', 20000.00, 'Efectivo', 2, 2, NULL),
	(3, '2026-03-18 15:29:48.185793', 143000.00, 'Efectivo', 2, 3, NULL),
	(4, '2026-03-18 15:51:20.629760', 1100000.00, 'Efectivo', 9, 5, NULL),
	(5, '2026-03-18 15:56:48.857554', 135678.40, 'Efectivo', 8, 4, NULL),
	(6, '2026-03-24 23:02:21.206529', 55000.00, 'Efectivo', 8, 7, NULL),
	(7, '2026-03-24 23:02:29.669720', 55000.00, 'Efectivo', 8, 6, NULL),
	(8, '2026-03-27 13:41:04.463647', 55000.00, 'Efectivo', 11, 8, NULL),
	(9, '2026-03-30 19:53:13.116138', 143000.00, 'Efectivo', 11, 9, NULL),
	(10, '2026-04-02 16:29:44.565191', 13200.00, 'Efectivo', 9, 10, NULL),
	(11, '2026-04-02 16:29:47.596618', 234557.40, 'Efectivo', 4, 11, NULL),
	(12, '2026-04-09 16:03:57.788947', 550000.00, 'Efectivo', 13, 12, NULL),
	(13, '2026-04-09 16:09:33.188683', 330000.00, 'Efectivo', 13, 13, NULL),
	(14, '2026-04-12 02:17:33.023114', 11000000.00, 'Efectivo', 18, 15, NULL),
	(15, '2026-04-12 02:20:17.638707', 135300.00, 'Efectivo', 18, 14, NULL),
	(16, '2026-04-23 21:47:55.639300', 19000.00, 'Efectivo', 17, 16, NULL),
	(17, '2026-04-24 00:03:28.292510', 12300.00, 'Efectivo', 18, 18, NULL),
	(18, '2026-04-24 00:03:28.301967', 12300.00, 'Efectivo', 18, 19, NULL),
	(19, '2026-04-24 00:03:28.313524', 12300.00, 'Efectivo', 18, 20, NULL),
	(20, '2026-04-24 00:03:28.321995', 12300.00, 'Efectivo', 18, 21, NULL),
	(21, '2026-04-24 00:06:40.224402', 3000.00, 'Efectivo', 2, 22, NULL),
	(22, '2026-04-24 00:06:40.227750', 3000.00, 'Efectivo', 2, 23, NULL),
	(23, '2026-04-24 00:06:40.230565', 3000.00, 'Efectivo', 2, 24, NULL),
	(24, '2026-04-24 00:06:40.233284', 3000.00, 'Efectivo', 2, 25, NULL),
	(25, '2026-04-24 00:07:21.883552', 100000.00, 'Efectivo', 9, 26, NULL),
	(26, '2026-04-24 00:07:21.887363', 100000.00, 'Efectivo', 9, 27, NULL),
	(27, '2026-04-24 00:07:21.891676', 100000.00, 'Efectivo', 9, 28, NULL),
	(28, '2026-04-24 00:08:04.405537', 5000.00, 'Efectivo', 2, 29, NULL);

-- Volcando estructura para tabla diamante_azul.queue_id_sequence
CREATE TABLE IF NOT EXISTS `queue_id_sequence` (
  `next_not_cached_value` bigint(21) NOT NULL,
  `minimum_value` bigint(21) NOT NULL,
  `maximum_value` bigint(21) NOT NULL,
  `start_value` bigint(21) NOT NULL COMMENT 'start value when sequences is created or value if RESTART is used',
  `increment` bigint(21) NOT NULL COMMENT 'increment value',
  `cache_size` bigint(21) unsigned NOT NULL,
  `cycle_option` tinyint(1) unsigned NOT NULL COMMENT '0 if no cycles are allowed, 1 if the sequence should begin a new cycle when maximum_value is passed',
  `cycle_count` bigint(21) NOT NULL COMMENT 'How many cycles have been done'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.queue_id_sequence: ~0 rows (aproximadamente)
INSERT INTO `queue_id_sequence` (`next_not_cached_value`, `minimum_value`, `maximum_value`, `start_value`, `increment`, `cache_size`, `cycle_option`, `cycle_count`) VALUES
	(1001, 1, 9223372036854775806, 1, 1, 1000, 0, 0);

-- Volcando estructura para tabla diamante_azul.usuarios_rol
CREATE TABLE IF NOT EXISTS `usuarios_rol` (
  `id_rol` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id_rol`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.usuarios_rol: ~3 rows (aproximadamente)
INSERT INTO `usuarios_rol` (`id_rol`, `nombre`) VALUES
	(1, 'Administrador'),
	(2, 'Empleado'),
	(3, 'Cliente');

-- Volcando estructura para tabla diamante_azul.usuarios_usuario
CREATE TABLE IF NOT EXISTS `usuarios_usuario` (
  `id_usuario` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `id_rol` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `email` (`email`),
  KEY `usuarios_usuario_id_rol_4b281f54_fk_usuarios_rol_id_rol` (`id_rol`),
  CONSTRAINT `usuarios_usuario_id_rol_4b281f54_fk_usuarios_rol_id_rol` FOREIGN KEY (`id_rol`) REFERENCES `usuarios_rol` (`id_rol`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla diamante_azul.usuarios_usuario: ~16 rows (aproximadamente)
INSERT INTO `usuarios_usuario` (`id_usuario`, `nombre`, `email`, `password_hash`, `id_rol`) VALUES
	(1, 'Admin', 'admin@gmai.com', 'pbkdf2_sha256$600000$yYj8F63ITi8rQ8OyiYxwUb$zseMkilVkOk5T3KR8h5vHXKYIYtGf9WAofN2dKgZt1Q=', 1),
	(4, 'Andres Guayabo', 'juego@gmail.com', 'pbkdf2_sha256$600000$9r9mGw3uOTTjvHGgtJ8oNv$daiiKvKqAw/pQzCn5kd57Vr+cyyeK/jkg3qtK+9LA0w=', 3),
	(6, 'tulio', 'prueba6@gmail.com', 'pbkdf2_sha256$600000$0P84Wlrh3OExwkcgkbIy5j$OvgLWgh8dfzdzCyFlUPdEy5jVaiGiuRv/TrPYiAsbEs=', 3),
	(12, 'aaaaaaaaaaa', 'gay@gmai.com', 'pbkdf2_sha256$600000$tv26IqRJu6QKNOK1auL43B$39Bw6l5wvRgbqgin0otxgNibfdGfcLFlbhADwos/hbM=', 3),
	(13, 'Yulieth', 'yuli@gmail.com', 'pbkdf2_sha256$600000$vF8dlyEQLLB2YBopOKvfgb$1AdrdDN+utB6DBB8L/GCPdnzEy9FGByYWUs9GMjuh0o=', 3),
	(14, 'Empleado', 'empleado@gmail.com', 'pbkdf2_sha256$600000$ch2DBkFWRT4Z4H5DtYUPO4$ludYtLOZoAiCornh1EH3EQBAidC0JfxEzz8T2gcaT5w=', 2),
	(15, 'nicolas', 'Z@gmail.com', 'pbkdf2_sha256$600000$6Jbf3TcD3ejIP3SQURxYL4$s7qC7LVPbRmJzmueY3rvV0a+xZQ4/sY4xItpSKh8L2k=', 3),
	(16, 'jhjyjjjjjj', 'jui@gmail.com', 'pbkdf2_sha256$600000$0MQB2yepDql4hUz5pvgcWB$aGsCzH4MCp3e6FTGAbFz1oX8cSdSOqsm01LcufpK778=', 3),
	(17, 'bueno', 'Bu@gmail.com', 'pbkdf2_sha256$600000$zeI0aCmXtrXjKigOGaIlHk$zS5wmYcXZINeWbqvbgTKXkrLhLtSWUogzw9O5y/qDCs=', 3),
	(18, 'Andres Felipe Vacca', 'hjfsk@gmail.com', 'pbkdf2_sha256$600000$3NC5uzvZa3DDqzxQ0ADRgz$oT27f8oscgwFmphiQsNQke5uM6huinGrUvtQZw8YFyg=', 3),
	(19, 'FDSFDSFSF', 'GFR@gmail.com', 'pbkdf2_sha256$600000$yMhGX1yYp3CcqEvyDqK7nf$NvcJcYXeXsczK1w9e41kamhfdRuRAEAnAYqvEbj9wPM=', 3),
	(20, 'Andres Felipe Vacca Jimenez', 'avacca853@gmail.com', 'pbkdf2_sha256$600000$WLmXISpVflXfF6UFKDV6oI$CSIaFSHaJVOBTbtzRTR/5tTAKEcYgybDaNWSTO2h2CE=', 1),
	(21, 'pruebaNoti', 'pruebaNoti1@gmail.com', 'pbkdf2_sha256$600000$t8b8wHPCzscMEHan4o4LJd$dLHKxZyvmuySDrfoGCESmz8LYwh9aRLkW1SgLXC9c6I=', 3),
	(22, 'prueba2', 'pruebaNoti2@gmail.com', 'pbkdf2_sha256$600000$l6LgU2vnC4XPKmknmHU73I$E+H3r9NwfcGHaN2z41CO4owBaECv5ueZ4I0vf8f2iaw=', 3),
	(23, '[TEST]', 'TEST@gmail.com', 'pbkdf2_sha256$600000$OUNZfeKBCCQ5gKRq8Zy6rw$0zdYt9S89LTtJwOwAJwQIWImP0g8sY5nGD5bY9qebxA=', 3),
	(24, 'Javier', 'javier123@gmail.com', 'pbkdf2_sha256$600000$sRwwYeou6q8vWj6FkQxkJG$QG7SqkFhuHCQzOQn1SXazYvx/cpZMWlKPjr1YAM66vs=', 3);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
