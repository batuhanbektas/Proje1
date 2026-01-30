

def Magaza(target):

    while True:
        print("""MAGAZADASIN
            NE SATIN ALMAK İSTERSİN:
            1-iksir
            2-cikis""")
        secim = input("Secimin: ")
        if(secim == "1"):
            if(target.potion < 10):
                target.potion += 1
                print(f"İksir:{target.potion} ")
            else:
                print("Envanterin Dolu. Daha Fazla Alamazsın.")
        elif(secim == "2"):
            break
        else:
            print("Gecersiz")