# Fuel consumption estimation
Instantaneous vehicle fuel consumption estimation using smartphones and recurrent neural networks.
___
Project developed by a group of system engineering students to explore the capabilities of the recurrent neural networks.

## Table of contents
- [Technologies](#Technologies)
- [Examples](#Examples)
- [References](#References)
- [Authors](#Authors)
- [License](#License)

## Technologies
The project was created with:
- Python 3.6.10 | Anaconda, Inc.
    - Keras 2.2.4-tf
    - Matplotlib 3.2.1
    - Numpy 1.18.1
    - Pandas 1.0.3
    - Scikit-Learn 0.22.2
- Java 11

## Examples
```jupyter
model = load_model('network_name.h5')
model.summary()
predictions = model.predict(inputs)
```
## References
- Kanarachos S., Mathew J., Fitzpatrick M. E. **[Instantaneous vehicle fuel consumption estimation using smartphones and recurrent neural networks](https://www.sciencedirect.com/science/article/pii/S0957417418307681?via%3Dihub)**. *Expert Systems With Applications 120 (2019) 436–447* 
- Chollet F. **Deep Learning with Python** *Manning Publications (2018)*
- https://stackabuse.com/solving-sequence-problems-with-lstm-in-keras/

## Authors
- [Rafał Górski](https://github.com/Qlas)
- [Michał Lisowski](https://github.com/Natsuvannen)
- [Wojciech Sikora](https://github.com/W-Sikora)
- [Jan Szkoda](https://github.com/Szkodzik)

## License
- MIT license
