# Family Finance (KivyMD) → Android APK (GitHub Actions Build)

## 1) हा ZIP GitHub वर upload करा
1. GitHub वर नवीन repo बनवा (उदा. `FamilyFinanceApp`)
2. Repo मध्ये हे सर्व files upload करा:
   - `main.py`
   - `buildozer.spec`
   - `.github/workflows/android.yml`

## 2) GitHub Actions ने APK build करा
1. Repo उघडा → **Actions** tab
2. डावीकडे “Build Android APK (Buildozer)” दिसेल
3. **Run workflow** (किंवा फक्त code push करा)

## 3) APK download
1. Build complete झाल्यावर त्या run वर क्लिक करा
2. खाली **Artifacts** मध्ये `FamilyFinance-APK` दिसेल
3. Download करा → ZIP extract करा → `.apk` file मिळेल

## 4) Mobile मध्ये install
- Settings → Security → **Install unknown apps** ON
- APK tap करून install

## Important (तुमच्यासाठी)
- app मध्ये internet वापरतो (`requests` + Google Script URL) म्हणून permissions already add केले आहेत.
- `package.domain` / `package.name` बदलायचे असतील तर `buildozer.spec` मध्ये बदला.
