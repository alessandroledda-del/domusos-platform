# Pipeline documentale v0.7

1. Upload file.
2. Salvataggio su storage S3.
3. Inserimento task Celery.
4. Scansione antivirus ClamAV.
5. Estrazione testo:
   - PDF nativo tramite pypdf;
   - immagine tramite Tesseract.
6. Classificazione documentale.
7. Aggiornamento metadati.
8. Notifica in-app.
9. Email utente.
10. Webhook `document.processed`.

## Limiti

I PDF scansione multipagina senza testo non vengono ancora convertiti
automaticamente in immagini pagina per pagina.
