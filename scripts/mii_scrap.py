from bs4 import BeautifulSoup
import requests

# https://mi-home.pl/wszystkie-produkty?p=8

#download pictures
def img_download(url):
    img_name = url.split('/')[-1]
    img_file = requests.get(url).content
    with open('products\\' + img_name, 'wb') as handler:
        handler.write(img_file)

#making json file
def info_saving(products, getPictures):
    progress = 0
    progressCounter = 0
    f = open("MIIproducts.json", "w", encoding="utf-8")
    f.write('{\n\t"products": [\n')
    for i in products:
        try:
            
            soup = BeautifulSoup(requests.get(i).content, 'html.parser')
            data = soup.find('div', {'class':'product-info-main block'})
            f.write("\t{\n")

            #name
            f.write('\t\t"name" : "'+data.find('h1',{'class':'page-title'}).text.strip().replace('"','\\"')+'",\n')

            #type
            f.write('\t\t"type" : "'+data.find('h2',{'class':'mi-product-type'}).text.strip()+'",\n')

            #sku
            f.write('\t\t"sku" : "'+soup.find('form',{'id':'product_addtocart_form'})['data-product-sku']+'",\n')

            #price
            f.write('\t\t"price" : "'+data.find('span',{'class':'price'}).text.strip().replace(' zł','').replace(' ','')+'",\n')

            #description
            f.write('\t\t"description" : "'+soup.find('div', {'itemprop': 'description'}).text.strip().replace('"','\\"').replace('\n',' ')+'",\n')

            #category
            script = soup.findAll('script',{'type':'text/x-magento-init'})
            word = 'product_breadcrumbs'
            for j in script:
                if word in j.text:
                    f.write('\t\t"category" : "'+j.text.strip().split('"name":"')[1].split('"')[0]+'",\n')
                    break

            #keywords
            f.write('\t\t"keywords" : "'+soup.find('meta',{'name':'keywords'})['content'].replace('\r',' ').replace('\n',' ').replace('"','\\"').split('\n')[0]+'",\n')

            #images
            for j in soup.findAll('script',{'type':'application/ld+json'}):
                if 'ImageGallery' in j.text:
                    images = j.text.split('"ImageGallery","image":"')[1].split('"}   ')[0].replace('\/','/').split(',')
                    f.write('\t\t"img" : [')
                    for x in images:
                        if getPictures:
                            img_download(x)
                        if x == images[-1]:
                            f.write('"'+ x.split('/')[-1] +'"')
                            break
                        f.write('"'+ x.split('/')[-1] +'",')
                    f.write('],\n')
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
                                if getPictures:
                                        img_download(image)
                                f.write('\t\t"img" : "'+ image.split('/')[-1] +'",\n')
                                break
        
                            id = k.text.split(id)[1].split('],"saleableProducts"')[0].split('[')[1].replace('"','').split(',')[0]
                            images = k.text.split('"images":')[1].split(str(id))[1].split('"videoUrl":null}]')[0].replace('\/','/').split('","full":"')
                            images.pop(0)

                            f.write('\t\t"img" : [')
                            for x in images:
                                imgLink = x.split('","caption"')[0]
                                if getPictures:
                                    img_download(imgLink)
                                if x == images[-1]:
                                    f.write('"'+ imgLink.split('/')[-1] +'"')
                                    break
                                f.write('"'+ imgLink.split('/')[-1] +'",')
                            f.write('],\n')
                            break


                        elif k == soup.findAll('script',{'type':'text/x-magento-init'})[-1]:
                            image = soup.find('meta',{'property':'og:image'})['description']
                            if getPictures:
                                    img_download(image)
                            f.write('\t\t"img" : "'+ 'not found' +'"\n')

            #dane techniczne
            techniczne = soup.find('table',{'class':'data table additional-attributes'}).findAll('tr')
            f.write('\t\t"attributes" : {\n')
            for x in techniczne:
                if x == techniczne[-1]:
                    f.write('\t\t\t"' + x.text.split('\n\n')[0].replace('\n','') + '" : "'+ x.text.split('\n\n')[1].replace('\n',', ').replace('"','\\"').replace('[email protected]','x') +'"\n')
                    break
                f.write('\t\t\t"' + x.text.split('\n\n')[0].replace('\n','') + '" : "'+ x.text.split('\n\n')[1].replace('\n',', ').replace('"','\\"') +'",\n')
            f.write('\t\t}\n')
            if (i == products[-1]):
                f.write('\t}\n')
            else:
                f.write('\t},\n')
        except:
            print("Error on: "+i)
        if i == products[progressCounter]:
            print(str(progress) + "% done")
            progress += 10
            if progressCounter+50 < len(products):
                progressCounter +=50 
                
    f.write(']}')
    f.close()

def link_scraping(url):
    products = []
    for i in range(14):
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
    print("MAKING JSON FILE")
    info_saving(products, True)
    print("DONE!")

if __name__ == "__main__":
    main()
