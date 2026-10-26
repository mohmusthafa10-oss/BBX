# Data Visualisation Assignment

## Part A — Chart Selection

### 1. Monthly revenue over three years — Line chart
I would use a line chart because it shows how revenue changes over time and helps identify overall trends, seasonal patterns, and sudden increases or decreases.

### 2. Revenue across eight product categories — Bar chart
I would use a bar chart because it makes it easy to compare revenue between the eight categories and identify which categories perform better or worse.

### 3. Distribution of customer ages — Histogram
I would use a histogram because it groups customer ages into intervals and shows where most customers fall, along with the shape and spread of the distribution.

### 4. Salary distribution across five departments — Box plot
I would use a box plot because it allows me to compare the median, spread, and possible outliers in salaries across all five departments.

### 5. Advertising spend versus sales — Scatter plot
I would use a scatter plot because it shows the relationship between advertising spend and sales and helps identify patterns, unusual observations, and possible correlations.

### 6. Correlation among ten numeric columns — Correlation heatmap
I would use a correlation heatmap because it displays the relationships between all pairs of numeric columns in one view, making strong positive and negative correlations easy to identify.

---

## Part B — The Dishonest Chart

Truncating the y-axis means starting it above zero instead of at zero. This can make a small difference between product categories look much larger than it actually is. For example, if two categories earn ₹90,000 and ₹95,000, starting the axis at ₹85,000 makes the difference appear enormous compared with showing the bars from zero. Readers may think one category is performing far better when the actual difference is only ₹5,000. This is especially misleading in a bar chart because people compare the lengths of the bars, and those lengths should represent the values fairly. A truncated axis is generally more defensible on a line chart because the main purpose is often to show changes and patterns over time, rather than compare bar lengths. However, it can still exaggerate changes. Therefore, the axis range should be clearly labelled, and the chart should never create a misleading impression of the data.

---

## Part C — Overplotting

Overplotting happens when many points overlap in a scatter plot, making it difficult to see the actual distribution of the data.

- **Alpha:** I would reduce the opacity of the points so overlapping areas become darker and denser regions are easier to identify.
- **Sampling:** I would plot a representative subset of the data to reduce clutter and make the overall pattern easier to see.
- **Hexbin:** I would group nearby points into hexagonal bins and use colour to represent the number of observations in each bin.

**My choice:** I would use a hexbin plot when the main goal is to understand the density of 100,000 points. It shows where observations are concentrated without drawing every point individually. If individual observations or outliers are important, I would also consider a transparent scatter plot or a representative sample.

---

## Part D — Anscombe's Quartet

Anscombe's quartet shows why summary statistics alone are not enough to understand a dataset. The four groups have very similar means, variances, and correlations, but their scatter plots look very different. One group may show a clear linear relationship, while another may contain a curved pattern, an unusual outlier, or most points clustered together with one influential observation. If we only compare numerical summaries, we might incorrectly assume that all four datasets behave in the same way. Plotting the data reveals these differences immediately. This is why I would always visualize data before drawing conclusions. Statistics are useful for summarizing information, but charts help us understand patterns, detect unusual observations, and avoid misleading interpretations.
