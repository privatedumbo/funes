# Blood Transfusion Service Center dataset

For the sake of this project, the dataset being used is not relevant. We should be able to use any dataset we want.

[Here](https://www.openml.org/search?type=data&sort=runs&id=1464&status=active) is the original dataset on OpenML.

Changes done to the dataset:

* Columns were renamed to be more expressive.
* The target column was renamed to `donor_type`. `1`s were casted to `True` and `2`'s were casted to `False` (which might be incorrect).
