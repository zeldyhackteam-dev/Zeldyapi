<?php
header('Content-Type: application/json; charset=utf-8');

$tckn = $_GET['tckn'] ?? '';
$file = '6masi.MYD';

if (!$tckn || !file_exists($file)) die(json_encode(["Success" => false, "Message" => "Hata"]));

// Dosyayı oku
$content = file_get_contents($file);

// 1. ADIM: Binary çöp karakterleri temizle (Sadece harf, rakam, boşluk ve bazı noktalama işaretlerini bırak)
$cleanContent = preg_replace('/[^\p{L}\p{N}\s\-\(\)\.\:]+/u', ' ', $content);

// 2. ADIM: Satırları ayır
$lines = explode("\n", $cleanContent);
$sonuclar = [];

foreach ($lines as $line) {
    $line = trim($line);
    // İçinde TCKN geçen satırı bul
    if (strpos($line, $tckn) !== false) {
        // Satırı boşluklardan temizle (fazla boşlukları teke düşür)
        $cleanLine = preg_replace('/\s+/', ' ', $line);
        
        // Veriyi bir blok olarak al, parçalamadan JSON'a ekle
        $sonuclar[] = $cleanLine;
    }
}

echo json_encode([
    "Success" => count($sonuclar) > 0,
    "Bulunan" => count($sonuclar),
    "Sonuclar" => $sonuclar,
    "Telegram" => "https://t.me/Zeldyy_here"
], JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
?>
