

#list1 = open("1.csv").readlines()
#print list1[0]


page ='class=houzzFrame><a class=houzz-share-button data-url="http://www.opad.com/estiluz-a-2403-tovier-wall-lamp.html" data-hzid=21e><a class=houzz-share-button data-url="http://www.opad.com/estiluz-a-2403-tovier-wall-lamp.html" data-hzid=2111 data'
start_link = 1
end_quote=0
while start_link >0:
    start_link = page.find('data-url="',end_quote)
    print start_link
    start_quote = page.find('"', start_link)
    print start_quote
    if start_quote == -1:
        break
    end_quote = page.find('"', start_quote+1)
    print end_quote
    url = page[start_quote+1:end_quote]

    print url
