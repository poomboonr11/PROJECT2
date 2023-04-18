0. ติดตั้ง Python 3, Pipenv, pgAdmin4,  ลงเครื่องให้เรียบร้อยก่อน

1. ดาวน์โหลดโปรเจ็คนี้ลงเครื่อง และ Restore ของ SQL ที่มีชื่อว่า Coffee_Shop ลงใน Data Base (ถ้าหากไม่สามารถกด Restore ได้ ให้ไปเพิ่ม Paths ใน Binary Paths ก่อน โดยใส่ตำแหน่งไฟล์ Bin ของ PostgreSQL )

2. เปิดโฟลเดอร์โปรเจ็คที่ชื่อว่า termproject_final ใน VSCode

3. เปิด VSCode Terminal

4. ติดตั้ง Packages ของโปรเจ็ค

        ---> python -m pip install Django

        ---> pip install pipenv

        ---> pipenv install

5. Activate pipenv environment

        ---> pipenv shell

6. จัดการ Database migtation 

        ---> python manage.py migrate

7. สร้าง Admin (Super user) ใส่ username email password และ password again อันนี้จะสามารถเข้าสู่ระบบได้

        ---> python manage.py createsuperuser

8. เปิดเว็บโปรเจค และสามารถลองเล่นบน http://localhost:8000/ ได้เลย

        ---> python manage.py runserver
