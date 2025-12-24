# GitHub'a Yükleme Talimatları

## Adım 1: GitHub'da Repository Oluşturun

1. [GitHub.com](https://github.com) adresine gidin ve giriş yapın
2. Sağ üst köşedeki **"+"** butonuna tıklayın
3. **"New repository"** seçeneğini seçin
4. Repository adını girin (örn: `yuz-tanima-sistemi`)
5. **Public** veya **Private** seçin
6. **"Create repository"** butonuna tıklayın
7. **ÖNEMLİ:** "Initialize this repository with a README" seçeneğini **İŞARETLEMEYİN** (zaten README.md var)

## Adım 2: Repository URL'ini Kopyalayın

Repository oluşturulduktan sonra, GitHub size bir URL gösterecek. Bu URL şuna benzer olacak:
```
https://github.com/kullaniciadi/repo-adi.git
```
Bu URL'yi kopyalayın.

## Adım 3: Projeyi GitHub'a Yükleyin

### Yöntem 1: Otomatik Script (Önerilen)

1. `github_push.bat` dosyasını çift tıklayın
2. Repository URL'ini yapıştırın ve Enter'a basın
3. İşlem tamamlanacaktır!

### Yöntem 2: Manuel Komutlar

PowerShell veya Command Prompt'u açın ve proje dizinine gidin, sonra şu komutları çalıştırın:

```bash
# Remote repository ekle (URL'yi kendi repository URL'inizle değiştirin)
git remote add origin https://github.com/kullaniciadi/repo-adi.git

# Branch'i main olarak ayarla
git branch -M main

# GitHub'a yükle
git push -u origin main
```

## Sorun Giderme

### "remote origin already exists" hatası alırsanız:
```bash
git remote set-url origin https://github.com/kullaniciadi/repo-adi.git
git push -u origin main
```

### "Authentication failed" hatası alırsanız:
GitHub artık şifre ile push kabul etmiyor. Şu seçeneklerden birini kullanın:

1. **Personal Access Token (Önerilen)**:
   - GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - "Generate new token" → "repo" yetkilerini seçin
   - Token'ı kopyalayın
   - Push sırasında şifre yerine bu token'ı kullanın

2. **GitHub CLI**:
   ```bash
   gh auth login
   ```

3. **SSH Key**:
   - SSH key oluşturup GitHub'a ekleyin
   - Repository URL'ini SSH formatına çevirin: `git@github.com:kullaniciadi/repo-adi.git`

## Başarılı Yükleme Sonrası

Repository'nizi GitHub'da görebilirsiniz:
```
https://github.com/kullaniciadi/repo-adi
```

Artık projeniz GitHub'da! 🎉

