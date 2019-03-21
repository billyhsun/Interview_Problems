class Hotel_Booking:

    def __init__(self, N, Q):
        self.days_until = {}
        self.prices = {}
        self.N = N
        self.Q = Q

    def disp_hotels(self):

        for a in self.Q:
            # a = a.split(',')
            self.days_until[a[0]] = int(a[1])

        for line in self.N:
            # line = line.split(',')
            location = line[0]
            supplier = line[1]
            price = float(line[2])

            days = self.days_until[location]

            if supplier == 'A' and days == 1:
                price = price * 1.5
            elif supplier == 'B' and days < 3:
                price = -1
            elif supplier == 'C' and days >= 7:
                price = price * 0.9
            elif supplier == 'D' and days < 7:
                price = price * 1.1

            price = round(price, 2)

            if price == -1:
                if location not in self.prices:
                    self.prices[location] = (["None"])
            else:
                if location not in self.prices:
                    self.prices[location] = [price]
                else:
                    self.prices[location].append(price)
                    if "None" in self.prices[location]:
                        self.prices[location].remove("None")

        for key, val in self.prices.items():
            val.sort()
            print(key, *val, sep=", ")

        return


if __name__ == "__main__":
    hotels = [['Toronto', 'A', 100.00], ['North York', 'B', 250],
              ['Kingston', 'C', 19.99], ['Toronto', 'D', 130],
              ['Kitchener', 'F', 25], ['Kitchener', 'F', 24],
              ['Kitchener', 'F', 25], ['Waterloo', 'B', 60],
              ['Waterloo', 'E', 45]]

    days_until = [['Toronto', 1], ['North York', 2],
                  ['Kingston', 10], ['Kitchener', 4],
                  ['Waterloo', 1]]

    HB = Hotel_Booking(hotels, days_until)
    HB.disp_hotels()
