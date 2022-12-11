from bs4 import BeautifulSoup
import requests
import os

git = 'https://github.com/EchoOfEden/obrazki/raw/main/products/'
# https://mi-home.pl/wszystkie-produkty?p=8

#download pictures
def img_download(url, index):
    img_name = url.split('/')[-1]
    img_file = requests.get(url).content
    if not os.path.exists('products'):
        os.mkdir('products')
        print("Directory Created ")
    if not os.path.exists('products\\'+str(index)):
        os.mkdir('products\\'+str(index))
        print("Directory " , index ,  " Created ")
    with open('products\\'+ str(index) +'\\' + img_name, 'wb') as handler:
        handler.write(img_file)

#making json file
def info_saving(products, getPictures):
    progress = 0
    progressCounter = 0
    productID = 1
    categoryID = 10
    customizable = 0
    f = open("MIIproducts.csv", "w", encoding="utf-8")
    c = open("MIIcategory.csv", "w", encoding="utf-8")
    f.write('"Product ID";Obraz;Nazwa;Indeks;Kategoria;"Cena (brutto)";Ilość;Widoczność;Opis;"Meta-opis";Tagi;Kombinacje;"Pozwól zamawiać";EAN;Atrybuty\n')
    c.write('"Category ID";Aktywny;Nazwa;Kategoria-rodzic;Głowna;Zdjęcie\n')
    c.close()
    for i in products:
        try:
            
            soup = BeautifulSoup(requests.get(i).content, 'html.parser')
            data = soup.find('div', {'class':'product-info-main block'})
            f.write(str(productID)+';')
            
            #images
            for j in soup.findAll('script',{'type':'application/ld+json'}):
                if 'ImageGallery' in j.text:
                    images = j.text.split('"ImageGallery","image":"')[1].split('"}   ')[0].replace('\/','/').split(',')
                    catimage = images[0]
                    for x in images:
                        if getPictures:
                            img_download(x, productID)
                        if x == images[-1]:
                            f.write(git + str(productID) + '/' + x.split('/')[-1] )
                            break
                        f.write(git + str(productID) + '/' + x.split('/')[-1] +',')
                    f.write(';')
                    break
                #wersja z wariantami
                elif j == soup.findAll('script',{'type':'application/ld+json'})[-1]:
                    for k in soup.findAll('script',{'type':'text/x-magento-init'}):
                        if '[data-role=swatch-options]' in k.text:
                            id = soup.find('input',{'name':'swatchOptions'})['value']
                            if 'Colour' in id:
                                id = id.split('"Colour":"')[1].split('"')[0]
                            elif 'color' in id:
                                id = id.split('color":"')[1].split('"')[0]
                            elif 'Color_name":"' in id:
                                id = id.split('Color_name":"')[1].split('"')[0]
                            else:
                                image = soup.find('meta',{'property':'og:image'})['content']
                                catimage = image
                                if getPictures:
                                        img_download(image, productID)
                                f.write(git + str(productID) + '/' + image.split('/')[-1] +';')
                                customizable = 1
                                break
        
                            id = k.text.split(id)[1].split('],"saleableProducts"')[0].split('[')[1].replace('"','').split(',')[0]
                            images = k.text.split('"images":')[1].split(str(id))[1].split('"videoUrl":null}]')[0].replace('\/','/').split('","full":"')
                            images.pop(0)

                            catimage = images[0].split('","caption"')[0]
                            for x in images:
                                image = x.split('","caption"')[0]
                                if getPictures:
                                    img_download(image, productID)
                                if x == images[-1]:
                                    f.write(git + str(productID) + '/' + image.split('/')[-1])
                                    customizable = 1
                                    break
                                f.write(git + str(productID) + '/' + image.split('/')[-1] +',')
                            f.write(';')
                            break


                        elif k == soup.findAll('script',{'type':'text/x-magento-init'})[-1]:
                            image = soup.find('meta',{'property':'og:image'})['description']
                            if getPictures:
                                    img_download(image, productID)
                            f.write(git + str(productID) + '/' + image.split('/')[-1] +';')
            
            #name
            f.write('"' + data.find('h1',{'class':'page-title'}).text.strip().replace('"','""')+'";')

            #sku
            f.write(soup.find('form',{'id':'product_addtocart_form'})['data-product-sku']+';')

            #category
            #"Category ID";Aktywny;Nazwa;Kategoria-rodzic;Głowna
            script = soup.findAll('script',{'type':'text/x-magento-init'})
            word = 'product_breadcrumbs'
            for j in script:
                if word in j.text:
                    category = j.text.strip().split('"name":"')[1].split('"')[0]
                    subcategory = data.find('h2',{'class':'mi-product-type'}).text.strip()
                    f.write(subcategory+';')
                    c = open("MIIcategory.csv", "r", encoding="utf-8")
                    if not category in c.read():
                        c.close()
                        c = open("MIIcategory.csv", "a", encoding="utf-8")
                        c.write(str(categoryID) + ';1;' +category + ';"Wszystkie produkty";0;' + git + str(productID) + '/' + catimage + '\n')
                        c.close()
                        categoryID += 1
                    c = open("MIIcategory.csv", "r", encoding="utf-8")
                    if not subcategory in c.read():
                        c.close()
                        c = open("MIIcategory.csv", "a", encoding="utf-8")
                        c.write(str(categoryID) + ';1;' +subcategory + ';' + category + ";0;" + git + str(productID) + '/' + catimage + '\n')
                        categoryID += 1
                    break


            #price
            f.write(data.find('span',{'class':'price'}).text.strip().replace(' zł','').replace(' ','').replace(',','.')+';')

            #quantity
            f.write('99;')

            #widoscznosc
            f.write('both;')

            #description
            f.write('"'+soup.find('div', {'itemprop': 'description'}).text.strip().replace('"','""').replace('\n',' ')+'";')
            #meta-description
            f.write('"'+soup.find('div', {'itemprop': 'description'}).text.strip().replace('"','""').replace('\n',' ')+'";')
    
            #tags
            f.write( soup.find('meta',{'name':'keywords'})['content'].replace('\r','').replace('\n','').replace('"','""')+';')
            
            #customizable
            f.write(str(customizable)+';')

            #pozwol zamawiac
            f.write("1;")

            #atrybuty
            swatch = soup.findAll('div',{'class':'swatch-opt'})
            
            #dane techniczne
            techniczne = soup.find('table',{'class':'data table additional-attributes'}).findAll('tr')
            for x in techniczne:
                cecha = x.text.split('\n\n')[0].replace('\n','') 
                wartosc =  x.text.split('\n\n')[1].replace('\n',', ').replace('"','\\"')
                if cecha == 'EAN':
                    f.write(wartosc + ';')
                if len(swatch) != 0:
                    if x == techniczne[-1]:
                        if cecha == 'Kolor':
                            f.write('Kolor:'+ wartosc)
                        break
                    if cecha == 'Kolor':
                        f.write('Kolor:'+ wartosc)

        except:
            print("Error on: "+i)
        if i == products[progressCounter]:
            print(str(progress) + "% done")
            progress += 10
            if progressCounter+50 < len(products):
                progressCounter +=50 
        f.write('\n')
        productID += 1
    f.close()

def link_scraping(url):
    products = []
    for i in range(1):
        soup = BeautifulSoup(requests.get(url + str(i+1)).content, 'html.parser')
        link = soup.findAll('a', {'class': 'product photo product-item-photo'})
        for j in link:
            if j.has_attr('href') and str(j['href']) != 'https://mi-home.pl/hybrydowe-szklo-do-mi-max-3':
                products.append(str(j['href']))
        print('Page ' + str(i+1) + ' links scrapped')

    return products
    
def main():
    url = "https://mi-home.pl/wszystkie-produkty?p="
    products = link_scraping(url)
    productsDummy = ['https://mi-home.pl/lexar-microsdxc-uhs-i-card-64gb-adapter']
    print("MAKING CSV FILE")
    info_saving(products, False)
    print("DONE!")

if __name__ == "__main__":
    main()
