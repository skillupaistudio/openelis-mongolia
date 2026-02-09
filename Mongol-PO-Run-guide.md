**Run Guide**

- **Backend Stack (Docker)**
  - `cd D:\B2B-GYALS\OpenELIS-Global-2-develop`
  - `.env` файлын `OE_DB_PASSWORD`, `ADMIN_PASSWORD` гэх мэт утгууд үнэн эсэхийг шалга.
  - `docker compose up -d` (эсвэл `docker-compose up -d`). Энэ нь Postgres, Tomcat (`oe.openelis.org`), FHIR, proxy (80/443) болон фронт-ын контейнеруудыг асаана.
  - Статус шалгах: `docker compose ps`. `openelisglobal-webapp`, `openelisglobal-proxy`, `openelisglobal-database` бүгд “Up” байвал OK.

- **Сертификат зөвшөөрөх**
  - Браузертаа `https://localhost` (proxy) хаягийг нэг удаа нээгээд “Advanced → Continue” хийж self‑signed сертификатыг зөвшөөр. Ингэснээр dev server‑ийн proxied API дуудлагууд блоклогдохгүй.

- **Frontend (CRA dev server)**
  - Шинэ mn.json ашиглахын тулд dev server-ийг гараар ажиллуулна:  
    ```
    cd D:\B2B-GYALS\OpenELIS-Global-2-develop\frontend
    npm install    # зөвхөн анх удаа
    npm start
    ```
  - `src/setupProxy.js` файл `/api/OpenELIS-Global` замыг `https://localhost` руу чиглүүлж байгаа тул `npm start`-ийг заавал энэ төслийн дотор ажиллуул.

- **Түгээмэл алдаа**
  1. **Нэвтрэх үед “JSON SyntaxError Unexpected token '<'”**  
     - Dev server-ийн proxy ажиллаж байгаа эсэхийг шалга: `frontend/src/setupProxy.js` оршин байх ёстой.  
     - Браузер дээр HTTPS сертификатыг зөвшөөрсөн эсэхээ дахин шалга (онцгойлон шинэ profile/шинэ браузер ашиглавал дахин зөвшөөрөх шаардлагатай).
  2. **Locale missing error** (`formatjs Missing locale data for "mn"`):  
     - Dev server restart хий (Ctrl+C → `npm start`). Polyfill импорт бүгд `src/index.js` дээр байна; restart хийгээгүй байхад хуучин build cache-нөөс polyfill ачаалж чадахгүй байж болно.
  3. **Backend login 401/HTML**:  
     - Docker контейнерууд ажиллаж байгаа үед `https://localhost/api/OpenELIS-Global/LoginPage` URL JSON биш HTML буцаана, энэ хэвийн. Харин dev server `http://localhost:3000/login` дээр байгаа Fetch хүсэлтүүд JSON (200) хариу авч байгаа эсэхийг Network tab-аас шалга. Хэрэв 401 эсвэл 404 бол proxy эсвэл сертификат тохируулга дутуу гэсэн үг.

- **Тест/Шалгалт**
  - Dev server ажиллаж байх үед `http://localhost:3000/login` руу орж `admin / adminADMIN!` (эсвэл өөр хэрэглэгч) ашиглан нэвтэр.
  - Network таб дээр `/api/OpenELIS-Global/ValidateLogin?apiCall=true` дуудаж байгаа, статус `200` бол OK. Амжилтгүй бол `Response` хэсгийн HTML‑ийг шалга; backend нэвтрэх хуудас буцааж байвал cookie/сессийн асуудал, 404 бол proxy зам буруу.

- **Сервер унтраах**
  - `npm start`-ийг зогсоох: терминал дээр `Ctrl+C`.
  - Docker stack: `docker compose down` (эсвэл `docker compose stop`).

Хэрэв эдгээр алхмыг дагаад тодорхой алдаа гарвал (Network request-ийн статус, консоль лог гэх мэт) screenshot эсвэл log-оор хэлээрэй; аль хэсэг дээр гацаад байгааг яг тодорхойлж туслахад амар.  - `src/setupProxy.js` файл `/api/OpenELIS-Global` замыг `https://localhost` руу чиглүүлж байгаа тул `npm start`-ийг заавал энэ төслийн дотор ажиллуул.

- **Түгээмэл алдаа**
  1. **Нэвтрэх үед “JSON SyntaxError Unexpected token '<'”**  
     - Dev server-ийн proxy ажиллаж байгаа эсэхийг шалга: `frontend/src/setupProxy.js` оршин байх ёстой.  
     - Браузер дээр HTTPS сертификатыг зөвшөөрсөн эсэхээ дахин шалга (онцгойлон шинэ profile/шинэ браузер ашиглавал дахин зөвшөөрөх шаардлагатай).
  2. **Locale missing error** (`formatjs Missing locale data for "mn"`):  
     - Dev server restart хий (Ctrl+C → `npm start`). Polyfill импорт бүгд `src/index.js` дээр байна; restart хийгээгүй байхад хуучин build cache-нөөс polyfill ачаалж чадахгүй байж болно.
  3. **Backend login 401/HTML**:  
     - Docker контейнерууд ажиллаж байгаа үед `https://localhost/api/OpenELIS-Global/LoginPage` URL JSON биш HTML буцаана, энэ хэвийн. Харин dev server `http://localhost:3000/login` дээр байгаа Fetch хүсэлтүүд JSON (200) хариу авч байгаа эсэхийг Network tab-аас шалга. Хэрэв 401 эсвэл 404 бол proxy эсвэл сертификат тохируулга дутуу гэсэн үг.

- **Тест/Шалгалт**
  - Dev server ажиллаж байх үед `http://localhost:3000/login` руу орж `admin / adminADMIN!` (эсвэл өөр хэрэглэгч) ашиглан нэвтэр.
  - Network таб дээр `/api/OpenELIS-Global/ValidateLogin?apiCall=true` дуудаж байгаа, статус `200` бол OK. Амжилтгүй бол `Response` хэсгийн HTML‑ийг шалга; backend нэвтрэх хуудас буцааж байвал cookie/сессийн асуудал, 404 бол proxy зам буруу.

- **Сервер унтраах**
  - `npm start`-ийг зогсоох: терминал дээр `Ctrl+C`.
  - Docker stack: `docker compose down` (эсвэл `docker compose stop`).

Хэрэв эдгээр алхмыг дагаад тодорхой алдаа гарвал (Network request-ийн статус, консоль лог гэх мэт) screenshot эсвэл log-оор хэлээрэй; аль хэсэг дээр гацаад байгааг яг тодорхойлж туслахад амар.