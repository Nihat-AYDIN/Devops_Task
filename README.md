Bu repoda verilen görevdeki tüm isterler yapılmıştır. 
Not :
  docker-compose up Komutunu root olarak çalıştırınız. 

Task kapsamında istenenler :
Üç adet Elasticsearch container’ı ayağa kaldırın ve bu 3 container’ı cluster olarak High Available çalışacak şekilde yapılandırın. Elasticsearch cluster yapılandırıldıktan sonra bir init script ile iller ve ülkeler adında iki index oluşturup her index’e 10 adet örnek document ekleyin.

Python ile bir web uygulaması geliştirin. Uygulamanın Docker container’ı içerisinde 4444 portundan çalışması / path’ine istek atıldığında “Merhaba Python!” yanıtını döndürmesi /staj path’ine istek atıldığında elasticsearch’de oluşturduğumuz iller index’inden rastgele bir il verisi döndürmesi gerekmektedir.

Go ile bir web uygulaması geliştirin. Uygulamanın Docker container’ı içerisinde 5555 portundan çalışması / path’ine istek atıldığında “Merhaba Go!” yanıtını döndürmesi /staj path’ine istek atıldığında elasticsearch’de oluşturduğumuz ülkeler index’inden rastgele bir ülke verisi döndürmesi gerekmektedir.

Metrik toplamak için prometheus container’ı kaldırın. Host’a ait metrikleri prometheus’a sunmak için Node exporter, container’lara ait metrikleri prometheus’a sunmak için Cadvisor kullanın. Prometheus’u Node Exporter ve Cadvisor metriklerini toplayacak şekilde konfigüre edin.

Topladığınız metrikleri görselleştirmek için Grafana container’ı kaldırın, kullanıcı login bilgilerini ayarlayın (User:admin Password:admin). Grafana container’ı başladığında yapılandırdığınız prometheus’un datasource olarak ekli olmasını, Node exporter (id:1860) ile Cadvisor exporter (id:14282) dashboard’larının grafana dashboards’da ekli olmasını ve dashboard’larda metriklerin gözüküyor olmasını sağlayın.

haproxy container’ı kaldırılıp 80 portuna gelen istekleri dinleyecek şekilde yapılandırın. kartaca.localhost adresine yapılan istekleri diğer container’lara yönlendirmek için haproxy kullanın. kartaca.localhost adresinin /pythonapp path’ine istek atıldığında istekleri python uygulamasının /staj path’ine yönlendirin, /goapp path’ine istek atıldığında istekleri go uygulamasının /staj path’ine yönlendirin. kartaca.localhost/grafana path’inden grafana arayüzüne ulaşılmasını sağlayın. haproxy’i sadece kartaca.localhost’a yapılan istekler için proxy uygulayacak şekilde yapılandırın, kartaca.localhost domain’i haricinde gelen istekler için 403 hatası dönmesini sağlayın.


DEĞERLENDİRME

Kontrol edeceğimiz sistemde kartaca.localhost ve kartaca2.localhost adresleri 127.0.0.1 ip adresini çözecek.
“docker compose up” komutu çalıştırıldıktan sonra elasticsearch cluster, python uygulama, go uygulama, haproxy, prometheus, grafana, nodeexporter, cadvisor container’larının ayağa kalkması, başka hiçbir yapılandırma yapmadan ilgili port ve path’lere yapılan isteklere aşağıdaki örneklerdeki gibi yanıt dönülmesi beklenmektedir;

$ echo "127.0.0.1 kartaca.localhost" >> /etc/hosts
$ echo "127.0.0.1 kartaca2.localhost" >> /etc/hosts

$ docker-compose up

$ curl localhost:4444
"Merhaba Python!"

$ curl localhost:4444/staj
{ "il": "tekirdag", "nufus": 1140200, "ilceler": ["hayrabolu", "malkara"] }

$ curl localhost:5555
"Merhaba Go!"

$ curl localhost:5555/staj
{ "ulke": "turkiye", "nufus": 84000000, "baskent":"ankara" }

$ curl kartaca.localhost/pythonapp
{ "il": "istanbul", "nufus": 16000000, "ilceler": ["beylikduzu", "esenyurt"] }

$ curl curl kartaca.localhost/goapp
{ "ulke": "fransa", "nufus": 67000000, "baskent":"paris" }

$ curl kartaca2.localhost/pythonapp
403 Forbidden

$ curl kartaca2.localhost/goapp
403 Forbidden

http://kartaca.localhost/grafana adresinden grafanaya login olunabilmeli ve Node exporter, Cadvisor exporter dashboard’ları ve toplanan metrikler görüntülenebilmeli.
