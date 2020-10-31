import matplotlib.pyplot as plt
import MineSweeper1 as ms1
import MineSweeper2 as ms2
import MineSweeper3 as ms3


def comparison2(sizes, minedensities, iterations):
    sizeData = {}
    for size in sizes:
        minedensitydata = {}
        for minedensity in minedensities:
            scorefor1 = 0
            time1 = 0
            scorefor2 = 0
            time2 = 0
            for iter in range(iterations):
                agent1 = ms1.MineSweeperPlay(size, minedensity, "A")
                result1 = agent1.letsplay()
                scorefor1 = scorefor1 + result1[1] / result1[0]
                time1 = time1 + result1[3] / (10 ** 3)
                agent2 = ms2.MineSweeper2Play(size, minedensity, "A")
                result2 = agent2.letsplay()
                scorefor2 = scorefor2 + result2[1] / result2[0]
                time2 = time2 + result2[3] / (10 ** 3)
            minedensitydata[minedensity] = {"Basic": [round(scorefor1 / iterations, 3), round(time1 / iterations, 2)],
                                            "KnowledgeBased": [round(scorefor2 / iterations, 3),
                                                               round(time2 / iterations, 2)]}
        sizeData[size] = minedensitydata
    return sizeData


def comparison4(sizes, minedensities, iterations):
    sizeData = {}
    for size in sizes:
        minedensitydata = {}
        for minedensity in minedensities:
            scorefor1 = 0
            time1 = 0
            scorefor2 = 0
            time2 = 0
            scorefor3 = 0
            time3 = 0
            scorefor4 = 0
            time4 = 0
            for iter in range(iterations):
                print(iter)
                agent1 = ms1.MineSweeperPlay(size, minedensity, "A")
                result1 = agent1.letsplay()
                scorefor1 = scorefor1 + result1[1] / result1[0]
                time1 = time1 + result1[3] / (10 ** 3)
                agent2 = ms2.MineSweeper2Play(size, minedensity, "A")
                result2 = agent2.letsplay()
                scorefor2 = scorefor2 + result2[1] / result2[0]
                time2 = time2 + result2[3] / (10 ** 3)
                agent3 = ms3.MineSweeper3Play(size, minedensity, "P", "A")
                result3 = agent3.letsplay()
                scorefor3 = scorefor3 + result3[1] / result3[0]
                time3 = time3 + result3[3] / (10 ** 3)
                agent4 = ms3.MineSweeper3Play(size, minedensity, "IP", "A")
                result4 = agent4.letsplay()
                scorefor4 = scorefor4 + result4[1] / result4[0]
                time4 = time4 + result4[3] / (10 ** 3)
            minedensitydata[minedensity] = {"Basic": [round(scorefor1 / iterations, 3), round(time1 / iterations, 2)],
                                            "KnowledgeBased": [round(scorefor2 / iterations, 3),
                                                               round(time2 / iterations, 2)],
                                            "Probabilistic": [round(scorefor3 / iterations, 3),
                                                              round(time3 / iterations, 2)],
                                            "Improved Probabilistic": [round(scorefor4 / iterations, 3),
                                                                       round(time4 / iterations, 2)]
                                            }
        sizeData[size] = minedensitydata
    return sizeData


def disp_data(data, varnames, xlable, ylabel, title, index):
    """
    This method is used to visualize data by displaying the graph
    :param index: 0 for score and 1 for time
    :param data: data to be plotted
    :param varnames: variables to be plotted
    :param xlable: x label
    :param ylabel: y label
    :param title: title
    """
    fig = plt.figure()  # Initializing figure
    ax1 = fig.add_subplot()
    ax1.set_xlabel(xlable)
    ax1.set_ylabel(ylabel)
    ax1.set_title(title)
    datakeys = list(data.keys())

    for var in varnames:
        score = list(map(lambda key: data.get(key).get(var)[index], data.keys()))
        ax1.plot(datakeys, score, label=var)
    ax1.legend(title="Agent")
    ax1.grid(True)


# {10: {0.2: {'Basic': [0.81, 11.16], 'KnowledgeBased': [0.905, 11.54], 'Probabilistic': [0.905, 353.07],
# 'Improved Probabilistic': [0.925, 434.44]}, 0.3: {'Basic': [0.727, 9.37], 'KnowledgeBased': [0.763, 12.03],
# 'Probabilistic': [0.88, 336.12], 'Improved Probabilistic': [0.883, 533.48]}}}

def reducedata(data, sizes, minedensities):
    dataToPlot = {}
    if len(sizes) == 1:
        dataToPlot = data.get(sizes[0])
    else:
        for key in data.keys():
            temp = data.get(key).get(minedensities[0])
            dataToPlot.update(temp)
    return dataToPlot


# print(comparison2([50], [0.2, 0.3, 0.4, 0.5, 0.6], 10))
print(comparison4([5, 10, 15], [0.4], 5))

# ms1 = ms1.MineSweeperPlay(10, 0.4, "A")
# result = ms1.letsplay()
# print(result)
