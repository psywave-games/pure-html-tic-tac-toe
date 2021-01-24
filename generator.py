import sys

with open('template') as file:
    template = file.read()

total_count = 0
total_win_x = 0
total_win_y = 0

class Stroke:
    def __init__ (self, url = ''):
        # Global variables
        global total_count
        global total_win_x
        global total_win_y
        global template

        # Construct            
        self.table = ['&nbsp;'] * 9
        self.links = ['false'] * 9
        total_count += 1

        # Analysis self url & Make Table
        for index in range (0, len(url), 2):
            self.table[int(url[index])] = url[index + 1]
            
        # State detect
        if self.is_winner():
            self.winner = True
            self.player = url[-1]
            self.layout = 'winner_' + self.player

        else: 
            self.winner = False
            self.player = 'o' if len(url) != 0 and url[-1] == 'x' else 'x'
            self.layout = 'player_' + self.player

        # Make others url's 
        for index in range(9):
            if self.table[index] == '&nbsp;' and not self.winner:
                self.links[index] = ''.join([(str(i) + self.table[i]) for i in range(9) if self.table[i] != '&nbsp;'])
                self.links[index] += str(index) + self.player

        # Block new stroke
        if self.winner:
            self.links = ['false'] * 9
            total_win_x += int(self.player == 'x')
            total_win_y += int(self.player == 'o')

        # Make webpage file
        url = 'index' if url == '' else url
        sys.stderr.write(f"[{total_count}] writing file {url}.html\n")
        with open(f"./multiplayer/{url}.html", "w") as file:
            html = template.format(layout = self.layout, links = self.links, table = self.table)
            html = html.replace('href="false"', '')
            html = html.replace('href="', 'href="{{ \'multiplayer/')
            html = html.replace('">&', '.html\' | relative_url }}">&')
            html = html.replace('">x', '.html\' | relative_url }}">x')
            html = html.replace('">o', '.html\' | relative_url }}">o')
            file.write(html)

        # Next 
        [Stroke(self.links[i]) for i in range(9) if self.links[i] != 'false']

    def is_winner(self):
        winner = False
        # Horizontal detect
        winner |= self.table[0] == self.table[1] and self.table[1] == self.table[2] and self.table[2] != '&nbsp;'
        winner |= self.table[3] == self.table[4] and self.table[4] == self.table[5] and self.table[5] != '&nbsp;'
        winner |= self.table[6] == self.table[7] and self.table[7] == self.table[8] and self.table[8] != '&nbsp;'
        # Diagonal detect
        winner |= self.table[0] == self.table[4] and self.table[4] == self.table[8] and self.table[8] != '&nbsp;'
        winner |= self.table[2] == self.table[4] and self.table[4] == self.table[6] and self.table[6] != '&nbsp;'
        # Verical detect
        winner |= self.table[0] == self.table[3] and self.table[3] == self.table[6] and self.table[6] != '&nbsp;'
        winner |= self.table[1] == self.table[4] and self.table[4] == self.table[7] and self.table[7] != '&nbsp;'
        winner |= self.table[2] == self.table[5] and self.table[5] == self.table[8] and self.table[8] != '&nbsp;'
        return winner

# bootstrap
Stroke()

# logs
sys.stderr.write(f"""[!] Done.
 > Files: {total_count}
 > Player X Winners: {total_win_x}
 > Player Y Winners: {total_win_y}
""")