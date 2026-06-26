<?php
/**
 * Local visual QA preview for the Ashira showroom pattern.
 *
 * Run from repo root:
 * php -S 127.0.0.1:8765
 * Open:
 * http://127.0.0.1:8765/docs/previews/ashira-showroom-preview.php
 */

function trailingslashit( $value ) {
	return rtrim( (string) $value, '/' ) . '/';
}

function get_template_directory_uri() {
	return 'http://127.0.0.1:8765';
}

function esc_url( $value ) {
	return htmlspecialchars( (string) $value, ENT_QUOTES, 'UTF-8' );
}

function rest_url( $path = '' ) {
	return 'http://127.0.0.1:8765/wp-json/' . ltrim( (string) $path, '/' );
}
?>
<!doctype html>
<html lang="he" dir="rtl">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Ashira שדה דב · NadLan showroom preview</title>
	<link rel="stylesheet" href="/assets/css/nadlan-project-showroom.css">
	<style>
		body {
			margin: 0;
			background: #f7f1e8;
			font-family: Arial, "Noto Sans Hebrew", sans-serif;
		}
		.nl-preview-header {
			position: sticky;
			top: 0;
			z-index: 20;
			display: flex;
			align-items: center;
			justify-content: space-between;
			padding: 12px 24px;
			border-bottom: 1px solid #e2d4c0;
			background: rgba(255, 253, 248, .94);
			backdrop-filter: blur(10px);
		}
		.nl-preview-header strong {
			color: #17130f;
		}
		.nl-preview-header nav {
			display: flex;
			gap: 18px;
			color: #5b5346;
			font-size: 14px;
		}
	</style>
	<script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/4.3.1/model-viewer.min.js"></script>
	<script defer src="/assets/js/nadlan-project-showroom.js"></script>
</head>
<body>
	<header class="nl-preview-header">
		<strong>NadLan</strong>
		<nav aria-label="ניווט תצוגה מקדימה">
			<span>פרויקטים</span>
			<span>מדריכים</span>
			<span>אנשי מקצוע</span>
			<span>יצירת קשר</span>
		</nav>
	</header>
	<?php include __DIR__ . '/../../patterns/project-showroom-ashira-sde-dov.php'; ?>
</body>
</html>
