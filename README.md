# AI Blog Yazarı Projesi

AI Blog Yazarı, fikirden yayınlamaya hazır makaleye kadar içerik üretim sürecini otomatikleştiren bir çözümdür.
Bu proje, Llama-3 dil modelinin gücünü, görev odaklı çalışan akıllı ajanlardan oluşan bir sistemle birleştirerek, tek bir komutla düzenli, anlaşılır ve kaliteli yazılar üretir.

Uygulama, Planlayıcı, Yazar ve Editör olmak üzere üç özel ajanın birlikte çalışmasıyla ilerler. Bu çok adımlı yöntem, yalnızca metin yazmakla kalmaz; aynı zamanda insan benzeri bir editörlük süreci izleyerek sonuçların kalitesini artırır.

Tam kapsamlı bir yaklaşımla geliştirilen bu proje; modern bir API altyapısı, kalıcı bir veritabanı ve etkileşimli bir kullanıcı arayüzünü bir araya getirmektedir.

---

## Projenin Amacı ve Özellikleri

Bu projenin temel amacı, içerik üretim sürecini otomatize etmek ve hızlandırmaktır. Kullanıcı tarafından verilen basit bir konudan yola çıkarak, çok adımlı bir yapay zeka ajan sistemi aracılığıyla tutarlı ve kaliteli metinler üretir.

### Ana Özellikler

*   **Çoklu Ajan Mimarisi:**
    *   **Planner Ajanı:** Verilen konuyu analiz eder ve mantıksal bir blog yazısı planı (içindekiler tablosu) oluşturur.
    *   **Writer Ajanı:** Oluşturulan plana sadık kalarak her bir başlık için detaylı ve akıcı bir taslak metin yazar.
    *   **Editor Ajanı:** Yazılan taslak metni dilbilgisi, imla ve üslup açısından gözden geçirerek metni yayınlanmaya hazır hale getirir.
*   **İnteraktif ve Kullanıcı Odaklı Arayüz:**
    *   Kullanıcı, yapay zekanın oluşturduğu planı yazma işlemine geçmeden önce düzenleyebilir.
    *   Yazım süreci sonunda, ilk taslak ile editörün düzenlediği nihai metin yan yana karşılaştırılarak yapay zekanın kattığı değer net bir şekilde görülebilir.
*   **Veri Kalıcılığı:**
    *   Oluşturulan tüm yazılar (plan, taslak ve nihai metin) bulut tabanlı bir PostgreSQL veritabanında saklanır.
    *   Kullanıcılar önceki oturumlarda oluşturdukları yazıları görüntüleyebilirler.
*   **Modern ve Ayrık Mimarî (Decoupled Architecture):** Frontend (Streamlit) ve Backend (FastAPI) katmanları birbirinden bağımsız olarak çalışır ve bir API üzerinden haberleşir. Bu, sistemin bakımını ve gelecekteki geliştirmeleri kolaylaştırır.

---

## Kullanılan Teknolojiler

Bu projenin hayata geçirilmesinde modern ve endüstri standardı teknolojiler kullanılmıştır.

### Backend (Sunucu Tarafı)
*   **Dil:** Python
*   **Web Framework:** FastAPI
*   **Yapay Zeka Modeli:** Trendyol/Llama-3-Trendyol-LLM-8b-chat-v2.0
*   **Veritabanı (ORM):** SQLAlchemy
*   **Veritabanı:** PostgreSQL (Neon.tech)
*   **Dağıtım Ortamı:** Google Colab

### Frontend (Kullanıcı Arayüzü)
*   **Framework:** Streamlit
*   **API İletişimi:** Requests
*   **Dağıtım Platformu:** Streamlit Community Cloud

### Altyapı ve Bağlantı
*   **Tünelleme Servisi:** Ngrok
*   **Versiyon Kontrol:** Git & GitHub

---

### Mimari ve Çalışma Prensibi

Bu proje, modern yazılım geliştirme prensiplerine uygun olarak tasarlanmış, **ayrık bir mimariye (decoupled architecture)** sahiptir. Bu, Frontend (kullanıcı arayüzü) ve Backend (sunucu mantığı) katmanlarının birbirinden tamamen bağımsız olduğu ve aralarında standart bir API (Uygulama Programlama Arayüzü) üzerinden iletişim kurduğu anlamına gelir. Bu yaklaşım, sistemin esnekliğini, ölçeklenebilirliğini ve bakım kolaylığını artırır.

Sistem dört ana katmandan oluşmaktadır:

**1. Frontend Katmanı (Streamlit Client)**

Kullanıcının doğrudan etkileşimde bulunduğu katmandır. Bu katmanın tek sorumluluğu, kullanıcıdan veriyi almak, bunu Backend'e iletmek ve Backend'den gelen veriyi kullanıcıya anlaşılır bir şekilde sunmaktır.

*   **Çalışma Ortamı:** Kullanıcının yerel bilgisayarı veya Streamlit Community Cloud.
*   **Temel Görevleri:**
    *   Kullanıcı girdilerini (örn: blog konusu) formlar aracılığıyla toplar.
    *   Kullanıcı eylemlerini (örn: butona tıklama) tetikleyici olarak kullanır.
    *   `requests` kütüphanesi aracılığıyla, Backend API'sine standart HTTP istekleri (GET, POST, PUT) gönderir.
    *   API'den dönen JSON formatındaki veriyi ayrıştırır (parse eder) ve `st.session_state` içinde yöneterek arayüzü dinamik olarak günceller.
    *   Uygulama mantığı veya yapay zeka işlemleri bu katmanda **gerçekleştirilmez**.

**2. Backend Katmanı (FastAPI Sunucusu)**

Projenin beyni ve iş mantığının merkezidir. Gelen tüm istekleri karşılar, gerekli işlemleri koordine eder ve bir yanıt döndürür.

*   **Çalışma Ortamı:** Google Colab (GPU destekli).
*   **Temel Görevleri:**
    *   **API Endpointleri:** `@app.post`, `@app.get` gibi dekoratörler aracılığıyla `/articles/`, `/articles/{id}/write` gibi URL yollarını tanımlar. Her bir endpoint, belirli bir işlevden sorumludur.
    *   **Veri Doğrulama:** `Pydantic` modellerini kullanarak gelen isteklerin yapısını ve veri türlerini otomatik olarak doğrular. Bu, hatalı veri girişini en başından engeller ve API güvenilirliğini artırır.
    *   **Orkestrasyon:** Bir istek geldiğinde, ilgili yapay zeka ajanını çağırır, ondan gelen çıktıyı alır ve ardından bu çıktıyı veritabanı katmanına kaydetmesi için yönlendirir. Tüm bu adımların sırasını ve koordinasyonunu yönetir.

**3. Yapay Zeka Çekirdeği (Ajan Mimarisi)**

İçerik üretiminin gerçekleştiği katmandır. Bu katman, genel amaçlı bir dil modelini (Llama-3), belirli görevler için uzmanlaşmış "ajanlara" dönüştürür.

*   **Temel Model:** `Trendyol/Llama-3-Trendyol-LLM-8b-chat-v2.0` modeli, metin anlama ve üretme yeteneği sağlar.
*   **Ajan Sınıfları (`Planner`, `Writer`, `Editor`):** Her bir sınıf, belirli bir göreve odaklanmış bir "sistem talimatı" (system prompt) içerir. Bu talimatlar, genel amaçlı modele o anki görevinin ne olduğunu, hangi formatta çıktı vermesi gerektiğini ve hangi kurallara uyması gerektiğini detaylıca anlatır. Bu yapı, modelin çıktılarının daha tutarlı ve hedefe yönelik olmasını sağlar.
    *   **Planner:** Yapısal ve hiyerarşik düşünme görevine odaklanır.
    *   **Writer:** Yaratıcı ve akıcı metin yazma görevine odaklanır.
    *   **Editor:** Analitik düşünme ve dilbilgisi kurallarına uyma görevine odaklanır.

**4. Veri Kalıcılığı Katmanı (PostgreSQL ve SQLAlchemy)**

Uygulamanın hafızasıdır. Üretilen tüm verilerin kalıcı olarak saklanmasından ve yönetilmesinden sorumludur.

*   **Veritabanı (PostgreSQL on Neon.tech):** Verilerin yapısal olarak (`users` ve `articles` tabloları gibi) saklandığı ilişkisel veritabanı sistemidir. Neon.tech, bu veritabanını bulutta yönetilen ve sunucusuz bir hizmet olarak sunar.
*   **ORM (Object-Relational Mapper - SQLAlchemy):** Bu katman, Python kodu ile SQL veritabanı arasında kritik bir tercüman görevi görür.
    *   **`models.py`:** Veritabanı tablolarının yapısını Python sınıfları olarak tanımlar. Bu sayede, geliştirici SQL sorguları yazmak yerine Python nesneleriyle çalışabilir.
    *   **İşlemler:** SQLAlchemy, `db.add(new_article)` gibi basit Python komutlarını, arka planda karmaşık `INSERT INTO ...` SQL sorgularına çevirir. Benzer şekilde, `db.query(models.Article).all()` komutunu `SELECT * FROM articles` sorgusuna dönüştürür. Bu, kodun daha okunabilir, sürdürülebilir ve veritabanından bağımsız olmasını sağlar.

---

### Adım Adım Bir İstek Akışı (Yeni Makale Oluşturma)

1.  **Kullanıcı Etkileşimi:** Kullanıcı, Streamlit arayüzüne bir konu girer ve "Plan Oluştur ve Başla" butonuna tıklar.
2.  **API Çağrısı:** Streamlit, `requests.post` kullanarak Backend'in `/articles/` endpoint'ine, konuyu bir sorgu parametresi (`query parameter`) olarak içeren bir HTTP isteği gönderir.
3.  **İstek Karşılama:** FastAPI, bu isteği alır ve `create_article_and_plan` fonksiyonunu tetikler.
4.  **Yapay Zeka Operasyonu:** Fonksiyon, `Planner` ajanını çağırır. Planner, Llama-3 modelini kullanarak verilen konuya özel bir blog planı metni üretir.
5.  **Veritabanı Kaydı:** Fonksiyon, gelen başlık ve üretilen plan ile bir `models.Article` Python nesnesi oluşturur. SQLAlchemy aracılığıyla bu nesne veritabanına bir `INSERT` sorgusu olarak gönderilir ve `articles` tablosuna yeni bir satır olarak eklenir.
6.  **Yanıt Döndürme:** Veritabanına başarıyla kaydedilen ve artık bir `id` içeren makale bilgisi, FastAPI tarafından JSON formatına serileştirilir ve HTTP yanıtı olarak Frontend'e geri gönderilir.
7.  **Arayüz Güncelleme:** Streamlit, gelen JSON yanıtını alır, `st.session_state`'e kaydeder, uygulama adımını bir sonrakine geçirir (`step = "edit_plan"`) ve `st.rerun()` komutuyla arayüzü güncelleyerek kullanıcıya plan düzenleme ekranını gösterir.

---

## Projeyi Yerelde Çalıştırma

### Ön Gereksinimler
*   Python 3.9+
*   Bir Hugging Face hesabı ve `HF_TOKEN`
*   Bir Ngrok hesabı ve `NGROK_TOKEN`
*   Bir Neon.tech (veya başka bir PostgreSQL) veritabanı ve bağlantı URL'si

### Backend'i Çalıştırma (Google Colab)

1.  Projenin Colab not defterini açın.
2.  Colab'in "Secrets" bölümüne aşağıdaki anahtarları ekleyin:
    *   `HF_TOKEN`: Hugging Face token'ınız.
    *   `NGROK_TOKEN`: Ngrok token'ınız.
    *   `DATABASE_URL`: PostgreSQL bağlantı URL'niz.
3.  Colab'deki tüm hücreleri sırasıyla çalıştırın. Tamamlandığında size bir Ngrok URL'si verilecektir. Bu URL'yi bir sonraki adım için kopyalayın.

### Frontend'i Çalıştırma (Lokal Bilgisayar)

1.  Bu GitHub deposunu klonlayın:
    ```bash
    git clone https://github.com/obenadak/ai-blog-writer.git
    cd ai-blog-writer
    ```

2.  Gerekli Python kütüphanelerini yükleyin:
    ```bash
    pip install streamlit requests
    ```

3.  `app.py` dosyasını bir kod düzenleyici ile açın ve `NGROK_BASE_URL` değişkenini, Colab'den aldığınız Ngrok URL'si ile güncelleyin.

4.  Uygulamayı başlatın:
    ```bash
    streamlit run app.py
    ```

---
