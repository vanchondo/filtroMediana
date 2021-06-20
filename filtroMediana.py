import cv2
import numpy as np
import statistics
import os

# Lee una matriz subset de la "matrix" pasada como parametro del tamaño especificado
# En caso de que la "matrix" original ya no contenga mas valores, los valores restantes
# en la matriz nueva se quedaran con el valor -1
def getSubMatrix(matrix, fromColumnIndex, toColumnIndex, fromRowIndex, toRowIndex):
    # Crea una lista conteniendo "colsSize" listas y cada una con "rowsSize" e inicializa cada elemento con -1
    windowMatrix = [[-1 for x in range(toColumnIndex - fromColumnIndex)] for y in range(toRowIndex - fromRowIndex)]
    totalColumns = matrix.shape[0]
    totalRows = matrix.shape[1]
    
    # print("["+ str(colsInitVale) + "," + str(rowsInitValue) + "] - ["+ str(colsSize) + "," + str(rowsSize) + "]")

    for x in range(fromColumnIndex, toColumnIndex):
        if totalColumns > x:
            for y in range(fromRowIndex, toRowIndex):
                if totalRows > y:
                    # print("Setting value on: ["+ str(x - colsInitVale) + "," + str(y - rowsInitValue) + "]")
                    windowMatrix[x - fromColumnIndex][y - fromRowIndex] = matrix[x][y]
    
    return windowMatrix

# Recibe una matriz de elementos, lo convierte en un arreglo unidimensional, elimina los valores -1 y calcula la mediana
# de ese arreglo
def calculateMedianForMatrix(matrix):
    # Convierte el arreglo bidimensional en un arreglo plano
    flattenWindow = np.concatenate(matrixWindow)

    # Elimina los elementos -1 que puedan existir dentro del arreglo para que no interfiera con el calculo de la mediana
    flattenWindow = [i for i in flattenWindow if i != -1]

    # Calcula la mediana del arreglo
    return statistics.median(flattenWindow)

# Escribe el valor en la "matrix" en el rango especificado
def setValueInMatrix(matrix, value, fromColumnIndex, toColumnIndex, fromRowIndex, toRowIndex):
    totalColumns = matrix.shape[0]
    totalRows = matrix.shape[1]

    for x in range(fromColumnIndex, toColumnIndex):
        if totalColumns > x:
            for y in range(fromRowIndex, toRowIndex):
                if totalRows > y:
                    matrix[x][y] = value
    
    return matrix

# Regresa una lista de archivos con la extension especificada en el directorio especificado
def getTestPicturesInPath(path, extension):
    pictures = []
    for file in os.listdir(path):
        if file.endswith(extension):
            pictures.append(os.path.join(path, file))
    
    return pictures


pictureList = []
picturePathList = getTestPicturesInPath("pictures/", ".jpeg")

print("Imagenes a procesar: " + str(len(picturePathList)))

for picturePath in picturePathList:
    print("Procesando: " + picturePath)

    img = cv2.imread(picturePath, cv2.IMREAD_GRAYSCALE)
    cleanImg = cv2.imread(picturePath, cv2.IMREAD_GRAYSCALE)

    cols = img.shape[0]
    rows = img.shape[1]

    windowSize = 5
    rowsInitValue = 0
    rowsReadLimit = windowSize

    for x in range(0, cols, 1):
        toColumnIndex = x + windowSize

        for y in range(0, rows, 1):
            toRowIndex = y + windowSize

            # Obtener sub matriz de windowSize x windowSize (3x3) de la matriz original
            matrixWindow = getSubMatrix(img, x, toColumnIndex, y, toRowIndex)

            # Calcular la mediana
            median = calculateMedianForMatrix(matrixWindow)

            # Guarda el valor de la mediana en cleanImg
            cleanImg = setValueInMatrix(cleanImg, median, x, toColumnIndex, y, toRowIndex)

    pictureList.append([img, cleanImg])
    
for picturePath, filteredPicture in zip(picturePathList, pictureList):
    print("Mostrando imagen: " + picturePath)
    compare = np.concatenate((filteredPicture[0], filteredPicture[1]), axis=1) #side by side comparison
    cv2.imshow(picturePath, compare)

cv2.waitKey(0)
cv2.destroyAllWindows