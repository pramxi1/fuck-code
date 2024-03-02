<?php

// โหลด Composer autoloader
require __DIR__ . '/dev/t.php';

// สร้างโครงสร้างข้อมูลที่ใช้ในการโหลดคลาสและไลบรารี
spl_autoload_register(function ($class) {
    // ตรวจสอบว่าคลาสอยู่ในเส้นทางที่ถูกต้องหรือไม่
    $file = __DIR__ . '/path/to/classes/' . str_replace('\\', '/', $class) . '.php';

    // ตรวจสอบว่าไฟล์คลาสมีอยู่หรือไม่ และโหลดไฟล์หากมี
    if (file_exists($file)) {
        require $file;
    }
});

