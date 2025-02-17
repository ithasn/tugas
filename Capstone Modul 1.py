#------------------------------------------------------------------------------------------------#
#                                       Import Module                                            #
#------------------------------------------------------------------------------------------------#

from tabulate import tabulate


#------------------------------------------------------------------------------------------------#
#                                     Define Initial Data                                        #
#------------------------------------------------------------------------------------------------#

# Note: Initial data di sini hanya contoh
tanggalSekarang = '2025-02-18' # Di real case kita bisa menggunakan fungsi datetime.now() dari modul datetime()
dataMobil = {
    'Nomor Polisi' : ['B 1234 XYZ', 'B 5678 ABC', 'B 9012 DEF', 'B 3456 GHI', 'B 7890 JKL', 'B 2345 MNO', 'B 6789 PQR', 'B 0123 STU', 'B 4567 VWX', 'B 8901 YZA'],
    'Tipe Mobil' : ['Toyota Agya', 'Daihatsu Xenia', 'Honda Brio', 'Toyota Kijang Innova', 'Mitsubishi Xpander', 'Suzuki Ertiga', 'Toyota Rush', 'Daihatsu Gran Max', 'Honda Mobilio', 'Toyota Agya'],
    'Status Sewa' : ['Disewa', 'Disewa', 'Tersedia', 'Tersedia', 'Disewa', 'Tersedia', 'Disewa', 'Tersedia', 'Disewa', 'Tersedia'],
    'Tanggal Sewa' : ['2025-02-17', '2025-02-16', '-', '-', '2025-02-17', '-', '2025-02-16', '-','2025-02-17', '-'],
    'Durasi Sewa' : [1, 3, '-', '-', 2, '-', 1, '-', 2, '-'],
    'Nama Penyewa' : ['Andi Setiawan', 'Dodo Wijoko', '-', '-', 'Gita Nurhayati', '-', 'Budi Santoso', '-', 'Rudi Hartono', '-']
}

#------------------------------------------------------------------------------------------------#
#                                      Define Function                                           #
#------------------------------------------------------------------------------------------------#

# Function untuk menghitung selisih hari dari dua buah tanggal berbentuk string dengan format 'YYYY-MM-DD'
# Dalam real case kita bisa menggunakan modul datetime, function ini hanya untuk memenuhi persyaratan capstone bahwa hanya diperkenankan import modul tabulate
def selisihTanggal(tanggal1, tanggal2):

    # Sub-function untuk menghitung total hari dari 1-Januari-0000 sampai tanggal yang diinput
    def totalHari(tanggal):

        # Memisahkan format tanggal dan mengkonversi menjadi integer ke masing-masing variabel berindex
        tahun, bulan, hari = map(int, tanggal.split('-')) # Contoh '2025-02-18'

        # Hitung total hari dari tahun 0000 AD sampai tahun yang diinput
        tahunKeHari = tahun * 365

        # Jumlah hari dalam setiap bulan (tidak memperhitungkan tahun kabisat)
        hariPerBulan = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        # Hitung total hari dari awa; bulan Januari sampai bulan terakhir sebelum bulan yang diinput (month-1)
        bulanKeHari = sum(hariPerBulan[:bulan])

        # Jumlahkan total hari dalam tahun + total hari dalam bulan + total hari sisanya
        total = tahunKeHari + bulanKeHari + hari 

        return total

    # Hitung total hari untuk kedua tanggal
    totalHari1 = totalHari(tanggal1)
    totalHari2 = totalHari(tanggal2)

    # Hitung selisih
    selisih = totalHari1 - totalHari2
    return selisih

# Function tambahan untuk memutuskan action plan jika ada penyewa yang telat mengembalikan
def actionPlan(dictData):

    # Meng-extract value dari tiap key dalam dictionary dictData,
    # menrangkai value dengan index yang sama dari masing-masing key,
    # serta mengkonversi hasil perangkaiannya menjadi list
    listValues = [list(index) for index in zip(*dictData.values())]

    # Menambahkan kolom 'Pengembalian' berdasarkan Tanggal Sewa dan Durasi Sewa
    for i in range(len(listValues)):
        tanggalSewa = listValues[i][3]
        durasiSewa = listValues[i][4]
        if tanggalSewa == '-':
            listValues[i].insert(5, '-') # Insert kolom 'Pengembalian' dengan value '-'
            actionPlan = '-'
        else:
            sisaSewa = selisihTanggal(tanggalSewa, tanggalSekarang) + durasiSewa
            if sisaSewa == 0:
                listValues[i].insert(5, 'Hari ini') # Insert kolom 'Pengembalian' dengan value 'Hari ini'
                actionPlan = '-'
            elif sisaSewa > 0:
                listValues[i].insert(5, str(sisaSewa) + ' hari lagi') # Insert kolom 'Pengembalian' dengan value 'n hari lagi'
                actionPlan = '-'
            else:
                listValues[i].insert(5, 'Telat ' + str(-sisaSewa) + ' hari') # Insert kolom 'Pengembalian' dengan value 'Telat n hari'
                actionPlan = 'Hubungi penyewa'
            listValues[i][4] = str(durasiSewa) + ' hari'

        # Menambahkan kolom 'Action Plan' pada tabel
        listValues[i].append(actionPlan) 

    # Menambah kolom pada headers mengikuti penambahan kolom pada values
    headers = list(dictData.keys()) + ['Action Plan']
    headers.insert(5,'Pengembalian')

    ziplistValues = [list(index) for index in zip(*listValues)] # Transpose tabel data
    dictDataModified = dict(zip(headers, ziplistValues)) # Mengubah format list menjadi dictionary dengan headers sebagai keys dan ziplistValues sebagai values

    return dictDataModified

# Function untuk memastikan input string yang dimasukkan berupa nomor polisi
def inputNopol():

    # Sub-function untuk memvalidasi string yang diinput berformat seperti nomor polisi
    def validasiNopol(nopol):
        
        # Jika string nopol terdiri dari 3 bagian
        if  len(nopol.split()) == 3:

            kodeWilayah = nopol.split()[0] # Contoh: 'B', 'A', 'KT'
            nomorRegistrasi = nopol.split()[1] # Contoh: '1234', '567', '1'
            kodeIdentifikasi = nopol.split()[2] # Contoh: 'JEO', 'CN', 'A'

            # Jika kode wilayah merupakan huruf dan terdiri dari 1-2 karakter, maka True
            if kodeWilayah.isalpha() and 1 <= len(kodeWilayah) <= 2:
                split1 = True
            else:
                split1 = False

            # Jika nomor registrasi merupakan angka dan terdiri dari 1-4 digit, maka True
            if nomorRegistrasi.isdigit() and 1 <= len(nomorRegistrasi) <=4:
                split2 = True
            else:
                split2 = False

            # Jika kode identifikasi merupakan hurud dan terdiri dari 1.3 karakter, maka True
            if kodeIdentifikasi.isalpha() and 1 <= len(kodeIdentifikasi) <= 3:
                split3 = True
            else:
                split3 = False
        
            # Outputnya adalah hasil operasi AND
            return split1 and split2 and split3

        # Jika string nopol tidak terdiri dari 3 bagian
        else:
            return False
    
    # Selama format belum benar, maka akan terus diminta memasukkan format yang benar
    while True:
        inputNopol = input('Masukkan nomor polisi (Contoh: "B 1234 XYZ"): ')
        print()

        if validasiNopol(inputNopol) == True:
            nomorPolisi = inputNopol.upper()
            break
        else:
            print('Format yang anda masukkan salah, masukkan format yang benar:')
            print('- Kode Wilayah terdiri dari 1 atau 2 huruf (Contoh: "B", "E", "KT")')
            print('- Nomor registrasi terdiri dari 1 sampai 4 angka (Contoh: "1234", "4043", "1346")')
            print('- Kode Identifikasi terdiri dari 1 sampai 3 huruf (Contoh: "JEO", "CN", "AW")')
            print('- Batasi setiap kode/nomor dengan [spasi]\n')

    # Output dari function adalah string nomor polisi yang sudah divalidasi
    return nomorPolisi

# Function untuk memastikan input string yang dimasukkan berupa tanggal dengan format "YYYY-MM-DD"
def inputTanggal(str):

    # Sub-function untuk mengecek apakah input string yang dimasukkan berupa tanggal dengan format "YYYY-MM-DD"
    def validasiTanggal(tanggal):

        # Jika string tanggal terdiri dari 3 bagian
        if len(tanggal.split('-')) == 3:
            tahun, bulan, hari = tanggal.split('-') # Split menjadi 3 dengan delimiter '-'

            # Jika tahun, bulan dan hari bukan angka, maka False
            if not (tahun.isdigit() and bulan.isdigit() and hari.isdigit()):
                cekTanggal = False
            
            # Jika tahun, bulan dan hari adalah angka, maka lanjutkan proses
            else:
                # Tahun minimal 1901
                intTahun = int(tahun)
                if intTahun > 1900:
                    cekTahun = True
                else:
                    cekTahun = False

                # Bulan harus antara 1 s.d 12
                intBulan = int(bulan)
                if 1 <= intBulan <= 12:
                    cekBulan = True
                else:
                    cekBulan = False

                # Hari harus antara 1 s.d 31, 1 s.d 30, ataupun 1 s.d 28 tergantung bulannya
                # Jika memenuhi persyaratan di atas, maka True, jika tidak, maka False
                intHari = int(hari)
                if intBulan in [1,3,5,7,8,10,12]:
                    if 1 <= intHari <= 31:
                        cekHari = True
                    else:
                        cekHari = False
                elif intBulan in [4,6,9,11]:
                    if 1 <= intHari <= 30:
                        cekHari = True
                    else:
                        cekHari = False
                elif intBulan in [2]:
                    if 1 <= intHari <= 28:
                        cekHari = True
                    else:
                        cekHari = False
                else:
                    cekHari = False
                
                cekTanggal = cekTahun and cekBulan and cekHari

        # Jika string tanggal tidak terdiri dari 3 bagian
        else:
            cekTanggal = False

        return cekTanggal

    # Input masukkan dari user, ulang terus sampai user memasukkan format yang benar    
    while True:
        inputTanggal = input(f'{str} (format "YYYY-MM-DD"): ')
        print()
        if validasiTanggal(inputTanggal) == True:
            tahun, bulan, hari = inputTanggal.split('-')
            tanggalFormatted = "-".join([tahun, bulan.zfill(2), hari.zfill(2)])
            return tanggalFormatted
        else:
            print('Format yang anda masukkan salah\nMasukkan dengan format "YYYY-MM-DD"\n')

# Function untuk menampilkan data berformat dictionary of lists menjadi tabel
def displayTabel(dictData):

    # Meng-extract value dari setiap keys pada dictionary, merangkainya dalam satu list[] sesuai indexnya (nomor urut) masing-masing
    listValues = [list(index) for index in zip(*dictData.values())]

    # Menambah nomor urut
    header = ['No.'] + list(dictData.keys())
    for i in listValues:
        i.insert(0,listValues.index(i)+1)

    # Menampilkan dalam garis-garis seperti tabel
    print(tabulate(listValues, headers=header, tablefmt='grid'))
    print()

# Function untuk mencari data mobil berdasarkan nomor polisi
def cariDataMobil(dictData):
    # Meng-copy keys dari dictData ke dictPencarian
    dictPencarian = {key:[] for key in dictData.keys()}
    nopol = inputNopol()

    # Mencari index lokasi Nopol tersebut pada list di key 'Nomor Polisi'
    if nopol in dictData['Nomor Polisi']:
        index = dictData['Nomor Polisi'].index(nopol)
        # Meng-copy seluruh values dalam dictData di index tersebut ke dalam values di dictPecarian
        for key in dictPencarian:
            dictPencarian[key].append(dictData[key][index])

    # Jika hasil pencarian kosong       
    if dictPencarian['Nomor Polisi'] == []:
        print('Nomor polisi tidak ditemukan')

    # Jika nomor polisi ada dalam list
    else:
        displayTabel(dictPencarian)
    print()

#Function untuk menu Tampilkan Data
def displayDataMobil(dictData):
    while True:
        print('''Menu tampilkan data:
    1. Tampilkan semua data mobil
    2. Cari data mobil berdasarkan nomor polisi
    3. Kembali
    ''')
        userInput = input('Pilih (1/2/3): ')
        print()

        if userInput == '1': # Tampilkan semua data mobil
            if not dictData: # Cek list kosong atau tidak
                print('Data kosong\n')
            else:
                print('Daftar Mobil Rental Autorentz Tangerang\n')
                print(f'Hari: Selasa\nTanggal: {tanggalSekarang}\n')
                displayTabel(dictData)

        elif userInput == '2': # Filter berdasarkan nomor polisi
            if not dictData: # Cek list kosong atau tidak
                print('Data kosong\n')
            else:
                cariDataMobil(dictData)

        elif userInput == '3':
            break

        else:
            print('Opsi yang anda masukkan tidak valid\n')

#Function untuk menambahkan data mobil baru ke dalam list
def registerMobilBaru(dictData):
    while True:
        print('''Menu register data:
    1. Register data mobil baru
    2. Kembali
    ''')
        userInput = input('Pilih (1/2): ')
        print()

        if userInput == '1': # Register data mobil baru
            nopol = inputNopol()

            if nopol in dictData['Nomor Polisi']:
                print('Mobil sudah terdaftar di database\n')
            else:
                tipeMobil = input('Masukkan merk dan tipe mobil: ').title()
                print()

                while True:
                    saveData = input('Simpan Data (y/t)?: ').lower()
                    print()

                    if saveData == 'y':
                        # Sisipkan nomor polisi dan tipe mobil baru ke dalam list
                        dictData['Nomor Polisi'].append(nopol)
                        dictData['Tipe Mobil'].append(tipeMobil)
                        dictData['Status Sewa'].append('Tersedia') # Karena mobil baru, sehingga nilai set awal 'tersedia'
                        dictData['Tanggal Sewa'].append('-') # Karena mobil baru, sehingga belum ada yang menyewa
                        dictData['Durasi Sewa'].append('-')
                        dictData['Nama Penyewa'].append('-')

                        print('Data berhasil disimpan!\n')
                        break

                    elif saveData == 't':
                        print('Data batal disimpan\n')
                        break
                        
                    else:
                        print('Opsi yang anda masukkan tidak valid\n')
                             
        elif userInput == '2': # Kembali
            break

        else:
            print('Opsi yang anda masukkan tidak valid\n')

# Function untuk mengupdate data mobil dalam list
def updateValues(dictData):
    while True:
        print('''Menu update data:
    1. Update data mobil
    2. Kembali
    ''')

        userInput = input('Pilih (1/2): ')
        print()

        if userInput == '1': # Update data mobil
            dictPencarian = {key:[] for key in dictData.keys()} # Meng-copy keys dari dictData ke dictPencarian, dengan values kosong
            nopol = inputNopol()
    
            # Jika nopol yang dimasukkan ada di list, catat indexnya
            if nopol in dictData['Nomor Polisi']:
                index = dictData['Nomor Polisi'].index(nopol)
        
                # 
                while True:
                    dictPencarian = {key:[dictData[key][index]] for key in dictData.keys()} # Meng-copy keys dan values dari dictData pada index tersebut ke dictPencarian 
                    displayTabel(dictPencarian)
                    dictPencarian = {key:[] for key in dictData.keys()} # Kosongkan kembali dictPencarian

                    lanjutUpdate = input('Lanjutkan update (y/t)?: ')
                    print()

                    if lanjutUpdate == 'y': # Lanjutkan update
                        namaKolom = input('Masukkan nama kolom yang ingin diupdate: ').title()
                        print()

                        if namaKolom in list(dictData.keys()):
                            if namaKolom == 'Nomor Polisi' or namaKolom =='Tipe Mobil':
                                print('Kolom tersebut tidak bisa diubah\n')
                        
                            elif namaKolom == 'Status Sewa':
                                if dictData['Status Sewa'][index] == 'Tersedia':
                                    print('Status saat ini "Tersedia"')
                                    while True:
                                        updateStatusSewa = input('Anda ingin update status sewa menjadi "Disewa" (y/t)?: ')
                                        print()
                                        if updateStatusSewa == 'y':
                                            # Update Status Sewa
                                            dictData['Status Sewa'][index] = 'Disewa'
                                            # Update Tanggal Sewa
                                            dictData['Tanggal Sewa'][index] = tanggalSekarang
                                            # Update Durasi Sewa
                                            while True:
                                                try:
                                                    durasiSewa = input('Masukkan durasi sewa (hari): ')
                                                    print()
                                                    dictData['Durasi Sewa'][index] = int(durasiSewa)
                                                    break
                                                except ValueError:
                                                    print('Masukkan input berupa angka\n')
                                                continue
                                            # Update Nama Penyewa
                                            dictData['Nama Penyewa'][index] = input('Masukkan nama penyewa: ').title()
                                            print('Data berhasil diupdate!\n')
                                            break
                                        elif updateStatusSewa == 't':
                                            print('Data batal diupdate\n')
                                            break                                        
                                        else:
                                            print('Opsi yang anda masukkan tidak valid\n')
                                else:
                                    print('Status saat ini "Disewa"')
                                    while True:
                                        updateStatusSewa = input('Anda ingin update status sewa menjadi "Tersedia" (y/t)?: ')
                                        print()
                                        if updateStatusSewa == 'y':
                                            dictData['Status Sewa'][index] = 'Tersedia'
                                            dictData['Tanggal Sewa'][index] = '-'
                                            dictData['Durasi Sewa'][index] = '-'
                                            dictData['Nama Penyewa'][index] = '-'
                                            print('Data berhasil diupdate!\n')
                                            break
                                        elif updateStatusSewa == 't':
                                            print('Data batal diupdate\n')
                                            break                                        
                                        else:
                                            print('Opsi yang anda masukkan tidak valid\n')

                            elif namaKolom == 'Tanggal Sewa':
                                if dictData['Status Sewa'][index] == 'Tersedia':
                                    print('Status mobil saat ini "Tersedia", mohon ubah dulu menjadi "Disewa"\n')
                                else:
                                    while True:
                                        tanggalSewaBaru = inputTanggal('Masukkan tanggal sewa: ')
                                        if selisihTanggal(tanggalSekarang, tanggalSewaBaru) < 0:
                                            print('Masukkan tanggal yang sudah lewat atau tanggal hari ini\n')
                                        else:
                                            break

                                    while True:
                                        updateTglSewa = input('Anda ingin update tanggal sewa (y/t)? :')
                                        print()
                                        if updateTglSewa == 'y':
                                            dictData['Tanggal Sewa'][index] = tanggalSewaBaru
                                            break
                                        elif updateTglSewa == 't':
                                            print('Data batal diupdate\n')
                                            break
                                        else:
                                            print('Opsi yang anda masukkan tidak valid\n')
                        
                            elif namaKolom == 'Durasi Sewa':
                                if dictData['Status Sewa'][index] == 'Tersedia':
                                    print('Status mobil saat ini "Tersedia", mohon ubah dulu menjadi "Disewa"\n')
                                else:
                                    while True:
                                        try:
                                            durasiSewaBaru = input('Masukkan durasi sewa (hari): ')
                                            print()
                                            intDurasi = int(durasiSewaBaru)
                                            break
                                        except ValueError:
                                            print('Masukkan input berupa angka\n')
                                            continue

                                    while True:
                                        updateDurasiSewa = input('Anda ingin update durasi sewa (y/t)? :')
                                        print()
                                        if updateDurasiSewa == 'y':
                                            dictData['Durasi Sewa'][index] = intDurasi
                                            break
                                        elif updateDurasiSewa == 't':
                                            print('Data batal diupdate\n')
                                            break
                                        else:
                                            print('Opsi yang anda masukkan tidak valid\n')

                            elif namaKolom == 'Nama Penyewa':
                                if dictData['Status Sewa'][index] == 'Tersedia':
                                    print('Status mobil saat ini "Tersedia", mohon ubah dulu menjadi "Disewa"\n')
                                else:
                                    namaPenyewaBaru = input('Masukkan nama penyewa: ').title()
                                    print()

                                    while True:
                                            updateNamaPenyewa = input('Anda ingin update Nama penyewa (y/t)? :')
                                            print()
                                            if updateNamaPenyewa == 'y':
                                                dictData['Nama Penyewa'][index] = namaPenyewaBaru
                                                break
                                            elif updateDurasiSewa == 't':
                                                print('Data batal diupdate\n')
                                                break
                                            else:
                                                print('Opsi yang anda masukkan tidak valid\n')
                    
                        else:
                            print('Mohon periksa kembali, tidak ada nama kolom tersebut\n')
                

                    elif lanjutUpdate == 't': # Kembali ke menu update
                        break

                    else:
                            print('Opsi yang anda masukkan tidak valid\n')
            else:
                print('Nomor polisi tidak terdaftar di database\n')
        elif userInput == '2':
            break

        else:
            print('Opsi yang anda masukkan tidak valid\n')

# Funtion untuk menghapus data Mobil
def deleteData(dictData):
    while True:
        print('''Menu hapus data:
    1. Hapus data mobil
    2. Kembali
    ''')

        userInput = input('Pilih (1/2): ')
        print()

        if userInput == '1': # Hapus data mobil
            nopol = inputNopol()

            # Mencari di index mana nomor polisi tersebut berada
            if nopol in dictData['Nomor Polisi']:
                index = dictData['Nomor Polisi'].index(nopol)

                # Konfirmasi delete data
                while True:
                    delData = input('Apakah anda yakin ingin menghapus data (y/t)?: ')
                    print()

                    if delData == 'y': # Menghapus values di index nopol yang diinput pada setiap keys
                        for key in dictData:
                            del dictData[key][index]
                        print('Data berhasil dihapus!\n')
                        break
                    elif delData == 't':
                        print('Data batal dihapus\n')
                        break
                    else:
                        print('Opsi yang anda masukkan tidak valid\n')
            else:
                print('Nomor polisi tidak ditemukan di database\n')
        
        elif userInput == '2': # Kembali
            break

        else:
            print('Opsi yang anda masukkan tidak valid\n')

# Function untuk menampilkan main menu
def displayMenu():
    print('Aplikasi Administrasi Mobil Rental Autorentz Tangerang')
    print('-'*44)
    print('''Silahkan pilih menu:
    1. Tampilkan data mobil
    2. Register data mobil baru
    3. Update status terkini mobil
    4. Hapus data mobil (write-off asset)
    5. Keluar
    ''')

def mainMenu():
    while True:
        dataMobilModified = actionPlan(dataMobil)

        displayMenu()
        pilihanMenu = input('Pilih menu (1/2/3/4/5): ')
        print()

        if pilihanMenu == '1':
            displayDataMobil(dataMobilModified) # Read Menu
        elif pilihanMenu == '2':
            registerMobilBaru(dataMobil) # Create Menu
        elif pilihanMenu == '3':
            updateValues(dataMobil) # Update Menu
        elif pilihanMenu == '4':
            deleteData(dataMobil) # Delete Menu
        elif pilihanMenu == '5':
            break
        else:
            print('Opsi yang anda masukkan tidak valid')
            print()

#------------------------------------------------------------------------------------------------#
#                                       Memanggil Menu                                           #
#------------------------------------------------------------------------------------------------#

mainMenu()