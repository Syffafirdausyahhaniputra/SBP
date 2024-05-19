# =================================================================
#   Nama: Syffa Firdausyah Hani Putra
#   NIM: 2241760005
#   Membuat kode program python untuk melakukan perhitungan MABAC
# =================================================================

# Saya menggunakan tabulate untuk mengubah tampilan output menjadi seperti table
# Jika belum pernah menggunakan tabulate, buka cmd lalu lakukan penginstalan tabulate dengan mengetikkan "pip install tabulate"

from tabulate import tabulate # type: ignore

# Data
data = [
    ["Kode", "C1", "C2", "C3", "C4"],
    ["D1", 90, 81, 89, 77],
    ["D2", 70, 80, 80, 85],
    ["D3", 85, 69, 78, 80],
    ["D4", 95, 80, 83, 80],
    ["D5", 82, 75, 85, 82],
    ["D6", 76, 85, 80, 87],
    ["D7", 72, 80, 75, 78],
    ["D8", 68, 72, 79, 86]
]

# Bobot
bobot = [
    ["C1", "C2", "C3", "C4"],
    [0.25, 0.3, 0.25, 0.2]
]

# Fungsi untuk menampilkan matriks dalam format tabel menggunakan tabulate
def print_matrix(matrix, title):
    print(title)
    print(tabulate(matrix[1:], headers=matrix[0], tablefmt="grid"))
    print()

# Tahap 1: Pembentukan matriks keputusan (X)
print("Tahap 1: Pembentukan matriks keputusan (X)")
print_matrix(data, "Matriks Keputusan (X)")

# Tahap 2: Normalisasi matriks keputusan (X)
min_values = [min(row[i] for row in data[1:]) for i in range(1, len(data[0]))]
max_values = [max(row[i] for row in data[1:]) for i in range(1, len(data[0]))]

normalized_data = [data[0]]  # header tetap sama
for row in data[1:]:
    normalized_row = [row[0]] + [(row[i] - min_values[i - 1]) / (max_values[i - 1] - min_values[i - 1]) for i in range(1, len(row))]
    normalized_data.append(normalized_row)

print("Tahap 2: Matriks Keputusan (X) Setelah Normalisasi:")
print_matrix(normalized_data, "Matriks Keputusan Setelah Normalisasi")

# Tahap 3: Perhitungan elemen matriks tertimbang (V)
weighted_matrix = [data[0]]  # header tetap sama
for row in normalized_data[1:]:
    weighted_row = [row[0]] + [row[i] * bobot[1][i-1] + bobot[1][i-1] for i in range(1, len(row))]
    weighted_matrix.append(weighted_row)

print("Tahap 3: Perhitungan Elemen Matriks Tertimbang (V):")
print_matrix(weighted_matrix, "Matriks Tertimbang")

G = ["G"]
for i in range(1, len(weighted_matrix[0])):
    column_values = [row[i] for row in weighted_matrix[1:]]
    product = 1
    for value in column_values:
        product *= value
    G.append(product ** (1/5))

print("Tahap 4: Matriks Area Perkiraan Batas (G):")
G_matrix = [[" "] + weighted_matrix[0][1:], G]
print_matrix(G_matrix, "Matriks Area Perkiraan Batas (G)")

# Tahap 5: Perhitungan matriks jarak elemen alternatif dari batas perkiraan daerah (Q)
Q = [["Alternatif"] + weighted_matrix[0][1:]]  # Header for the Q matrix

# Calculate Q for each alternative
for i in range(1, len(weighted_matrix)):
    Q_row = [weighted_matrix[i][0]]  # Alternative ID
    for j in range(1, len(weighted_matrix[i])):
        Q_value = weighted_matrix[i][j] - G[j]
        Q_row.append(Q_value)
    Q.append(Q_row)

print("Tahap 5: Matriks Jarak (Q):")
print_matrix(Q, "Matriks Jarak (Q)")

# Tahap 6: Perangkingan alternatif
ranking_scores = {}  # Dictionary to store the ranking scores for each alternative

# Calculate the sum for each alternative
for row in Q[1:]:
    alternative = row[0]
    score = sum(row[1:])  # Summing up all values except the first one (alternative ID)
    ranking_scores[alternative] = score

# Print the ranking scores
print("Tahap 6: Perangkingan Alternatif")
ranking_data = [["Alternatif", "Score"]] + [[alternative, score] for alternative, score in ranking_scores.items()]
print(tabulate(ranking_data, headers="firstrow", tablefmt="grid"))
print()

# Sort the ranking scores in descending order (nilai terbesar ke terkecil)
sorted_ranking = sorted(ranking_scores.items(), key=lambda x: x[1], reverse=True)

# Print the sorted ranking
print("Peringkat Alternatif:")
sorted_ranking_data = [["Rank", "Alternatif", "Score"]] + [[rank, alternative, score] for rank, (alternative, score) in enumerate(sorted_ranking, start=1)]
print(tabulate(sorted_ranking_data, headers="firstrow", tablefmt="grid"))
