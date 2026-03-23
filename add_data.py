import sqlite3

def add_demo_data():
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()
    
    demo_jobs = [
        ('Python Developer', 'Google', 'Backend APIs aur automation scripts likhne ke liye experience chahiye.'),
        ('Java Developer', 'TCS', 'Enterprise level applications aur Spring Boot par kaam karna hoga.'),
        ('Web Designer', 'Zomato', 'HTML5, CSS3 aur Bootstrap ka use karke clean UI banana hai.'),
        ('Data Analyst', 'Microsoft', 'SQL aur PowerBI ka use karke business insights nikalne hain.'),
        ('Android Developer', 'PhonePe', 'Kotlin aur Android Studio mein expertise honi chahiye.'),
        ('Cybersecurity Intern', 'Cisco', 'Network monitoring aur vulnerability assessment ka basic knowledge.'),
        ('React Developer', 'Meta', 'Frontend development using React.js aur Redux.'),
        ('Software Engineer', 'Amazon', 'Scalable web services aur cloud architecture par kaam karein.'),
        ('Full Stack Developer', 'Flipkart', 'MERN Stack (MongoDB, Express, React, Node) par pakad honi chahiye.'),
        ('Network Engineer', 'Jio', 'Router configuration aur network troubleshooting handle karni hogi.')
    ]

    cursor.executemany("INSERT INTO jobs (title, company, description) VALUES (?, ?, ?)", demo_jobs)
    conn.commit()
    conn.close()
    print("10 Demo Jobs successfully add ho gayi hain!")

if __name__ == '__main__':
    add_demo_data()