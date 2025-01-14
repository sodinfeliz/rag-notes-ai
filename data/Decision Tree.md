---
association:
  - "[[@52.31 Supervised Learning|52.31 Supervised Learning]]"
  - "[[Random Forest]]"
---
# Decision Tree

> [!image]- Visualization of a decision tree:
> ![[Decision-Tree-visualization.png]]

A **Decision Tree** is a widely used machine learning model that makes decisions based on a series of <u>questions about the features of the data</u>. The model is structured like a [[tree]]:

1. **Nodes**: Each node represents a feature (or attribute) in the dataset.
2. **Branches**: Each branch represents a <u>decision rule</u> based on the feature's value.
3. **Leaves**: Each leaf node represents the <u>outcome</u> or <u>class label</u>.

The tree splits the data into subsets based on the value of input features, starting from the root node and moving down to the leaf nodes. This process continues recursively, forming a tree structure of decisions.

## Types of Decision Tree

| Type           | Criteria                                        | Evaluation      |
| -------------- | ----------------------------------------------- | --------------- |
| Classification | [[Gini Impurity]], [[Shannon Entropy\|Entropy]] | Majority Voting |
| Regression     | [[Mean Squared Error]] (MSE)                    | Average Values  |

- \*Both types of decision tree are collectively called the <u>Classification and Regression Tree</u> (**CART**).

## Vanilla Algorithm of Decision Tree

### Choosing the Criteria

According to the types of decision tree to choose the criterion for splitting nodes (e.g., Gini impurity, entropy for classification, mean squared error for regression).

For **classification tasks**, the common criteria are:

- [[Gini Impurity]]: Measure the impurityof a node. Lower values are better as they indicate purer nodes: $$\text{Gini} = 1 - \sum\limits_{i=1}^{C} p_{i}^{2}$$where $p_i$ is the proportiton of samples belonging to class $i$ in the node.
- [[Shannon Entropy|Entropy]]: Measures the information content (uncertainty) of a node. Lower entropy indicates better splits: $$\text{Entropy} = -\sum\limits_{i=1}^{C} p_{i} \log_{2}(p_{i})$$ where $p_i$ is the proportiton of samples belonging to class $i$ in the node.

For **regression tasks**, the common criterion is:

- [[Mean Squared Error]] (MSE): Measure the variance within a node. Lower MSE indicate better splits:$$\text{MSE} = \frac{1}{N}\sum\limits_{i=1}^{N} {(y_{i} - \bar{y})}^{2} $$where $y_i$ is the actual value and $\bar{y}$ is the mean value of the node.

### Stopping Criteria

The algorithm stops splitting when one or more of these conditions are met:

| Criteria                                           | Parameters in [[Scikit-learn]] |
| -------------------------------------------------- | ------------------------------ |
| Maximum depth is reached                           | `max_depth`                    |
| Minimum number of samples in a node is reached     | `min_samples_leaf`             |
| Minimum number of samples required to split a node | `min_samples_split`            |
| All samples in a node belong to the same class     | –                              |
| Further splitting would not improve the metric     | `min_impurity_decrease`        |

### Recursive Splitting

- Calculate the impurity of the current node
- Determine all possible split points for EVERY feature
	- **Numerical** Features: 
		- Split points are the midpoints between consecutive values.
		- **Example**: `[2, 3, 5]`
		- **Possible Split Points**: `2.5`, `4`
	- **Categorical** Features: 
		- Possible ways to split the categories into two subsets.
		- Example: `{A, B, C, D}`
		- **Possible Split Points**: {A} vs {B,C,D}, {A, C} vs {B, D}, etc.
- Calculate the weighted average impurity:
	- For each possible split point, calculate the <u>weighted average impurity</u> of the children nodes. Use the formula$$ \text{Weighted Impurity} = \frac{n_l}{n_t} \times \text{Impurity of Left Child} + \frac{n_r}{n_t} \times \text{Impurity of Right Child}$$ where $n_t$ is number of samples at the current node, $n_l$ is the number of samples in the left child, and $n_r$ is the number of samples in the right child.
- Select the best split points: 
	- Identify the split point that results in the minimum weighted average impurity.
- Calculate the impurity decrease: 
	- After finding the minimum weighted average impurity, compute the **impurity decrease** to determine whether to stop splitting. $$\text{Impurity Decrease} = \frac{n_\text{t}}{N} \Big(\text{Impurity of Current Node} - \text{Weighted Impurity}\Big)$$where $N$ is the total number of samples.
	- Compare the impurity decrease to the `min_impurity_decrease`. If the impurity decrease is sufficient, proceed with the split; otherwise, stop splitting and consider the current node a leaf.
- Choose the best feature and split point: 
	- After calculating the weighted average impurity for every feature, choose the one with the maximum impurity decrease.
- Recursively apply the splitting process:
	- Repeat the steps for the left and right child nodes until [[Decision Tree#Stopping Criteria|stopping criteria]] are met.

## Algorithms

- [[Iterative Dichotomiser 3|ID3]]: An algorithm for building decision trees using information gain as the splitting criterion. It is suitable for categorical attributes.
- [[C4.5]]: An improved version of ID3 that uses gain ratio for splitting, handles continuous attributes, includes pruning, and can manage missing values.

## See also …

- [[Stump]]
- [[Lazy Decision Tree]]

