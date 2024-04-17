# *Unlocking Pricing Mastery: The Blueprint*


<center><img src="strategy_price_cover.webp" alt="price-strategy" width="400"></center>


- [Why is important?](#why-is-important?)
- [Net Revenue Management](#Net-Revenue-Management)
- [The roadmap](#the-roadmap)
- [Case study](#case-study)
   + [data exploring](#data-exploring)
- [ML models](#ml-models)
   + [building the model](loyalty_drivers.ipynb)


## Why is important?


A net revenue management agenda is crucial for any organization as it's all about boosting revenue by smartly handling pricing, promotions, and product availability to make the most profit. 

Here's why it's so important:

- **Maximizing Profits:** It helps ensure we're earning as much as possible from our products or services without turning away customers with overly high prices.

- **Optimizing Product Availability:** By making sure our products are available when and where customers want them, we avoid losing sales due to shortages or excess inventory.

- **Balancing Demand and Supply:** We can match our product supply with customer demand, adjusting prices and promotions to encourage sales during slow times or manage demand during busy periods.

- **Enhancing Customer Satisfaction:** Offering the right products at the right price and time improves customer happiness, leading to repeat business and positive word-of-mouth.

- **Competitive Advantage:** It gives us an edge by allowing us to respond swiftly to market changes, outsmart competitors, and grab more market share.

- **Data-Driven Decision Making:** By analyzing data on customer behavior, market trends, and competitor actions, we can make informed decisions to boost revenue and profits.

In a nutshell, a net revenue management agenda is absolutely essential for any organization because it helps us achieve our strategic and financial goals effectively.


## Net Revenue Management


<img src="main_points.png" alt="main-points" width="650">


The points mentioned above highlight why implementing a **net revenue management (NRM)** agenda is crucial. However, what's equally important is understanding how to develop such an agenda. While **pricing** is the ultimate output of the program, the key lies in identifying opportunities through data analysis for **revenue growth.** 

Therefore, the most critical aspect is harnessing the power of data. Ultimately, **NRM** empowers organizations to effectively leverage available data for sustainable growth. In this article, we'll delve into the essential steps and considerations for begin to develop a successful NRM agenda that drives revenue growth through data utilization.


## The roadmap


*`1.-Brand portfolio pricing:`*
- The initial step in the revenue management roadmap involves understanding how pricing impacts demand.At this stage, it's crucial to consider factors like equity and our competitive advantage within the segment.Conducting an elasticity test is also essential to gauge market sensitivity to price changes. This helps answer the pivotal question:<br><center>**"Which is the right price?"**.</center><br> Also it's important to consider both market prices and competitor pricing during this phase of the roadmap.

*`2.-Price architecture`*
- another thing to consider is the next, the architecture of the price is important how need to be estructured the price and which price is the most attractive? in the last question is very common in some business to see prices with odd ending and during promotions times with 99 or 95 endings and this is very important because despite the elasticity is important to consider de psicologycal pricing and the current stage which is the most attractive price, also we need to consider that the endings not increase the demand all the time and not work by itself in all products in the article "Estimating the effect of odd pricing" from Philip Gendall show us that the price ending 99 is more effective for low-priced and fast-moving products
  
*`3.-Mix management`*
- The mix management stage is super important because we need a smart plan that considers all our different products (if we have them). This helps us find the best mix and make the most money. Remember how we talked about setting prices like \\$9.99 or \\$9.95 earlier? Well, that matters here too. We need to use different math tricks, like optimization algorithms, to find the best balance for all the stuff we're selling. We can use tools like linear programming to figure out the best way to do this.

*`4.-Promotion management`*
- When planning how to make more money, we need to think about promotions too. To do this, we can use a tool called marketing mix analysis. This helps us understand how things like advertising, prices, promotions, and discounts affect sales.

  It's really important to understand how each of these things affects how much people want to buy, and to know when, where, and why they decide to buy. This helps us see what makes people want to buy more, and what doesn't.

  To figure this out, we can use something called causal inference. This helps us understand if things like discounts actually make people buy more, or if things like Christmas make people want to buy more.
  
*`5.-Trade terms management`*
- In the final step of many businesses, we need to make sure that our commercial terms match our prices. In businesses that sell to other businesses (B2B), we can create a pricing plan with different levels. We start with a basic price, then adjust it based on how much demand there is. The goal is to come up with a pricing plan where both sides feel like they're getting a good deal.


<img src="roadmap.png" alt="roadmap" width="850">


## Case study


<center><img src="gas_station.webp" alt="gas-price" width="400"></center>


We're studying a gas site that sells three products. For this example, let's focus on just one product. We want to understand how its price affects demand and how other factors like holidays, days of the week, and even the impact of the COVID pandemic play a role.

Here's what our data includes:
- Date
- Day of the week
- Month
- Year
- Product
- Hour
- Volume sold
- Number of transactions
- Average volume per transaction
- Price
- Number of rainy days in the month
- Weekday number
- Weekend flag (assuming Thursday through Sunday)
- Holiday name

It's important to know that this data is synthetic and doesn't perfectly represent how a real business behaves.


### Data exploring


Price optimization means using past information to figure out the best price for something, like a product or service, that makes the most money for a company. Many things, such as who buys it, how much it costs to make, and what people say in surveys, affect how things should be priced. It also depends on the type of business and what it sells.

Companies often add new things or make improvements to make their product better, but this costs time, effort, and affects how people see the company.

So, it's really important to get the price right. If it's too high, people won't buy it, and if it's too low, the company loses money. Price optimization helps businesses find the right balance so they can make money and keep their customers happy.


*`correlation among variables`*

In this case study, we're sticking to the plan we made earlier. Our first task is to check out the data. When we start digging into the data, it's important to remember that just because two things seem connected, it doesn't mean one causes the other. But, figuring out how different things are linked can still tell us a lot.

For example, we're examining how prices relate to things like rainy days or holidays. We might check if prices change depending on who sets them first, or if sales change on weekends.


<center><img src="correlation.png" alt="correlation" width="650"></center>


The chart above shows that there's not a strong connection between prices and sales. The correlation between them is almost 0, with a value of 0.07. This means there's not much special going on there. On the other hand, rainy days seem to have a slight negative connection with sales, suggesting that when it rains, sales might drop a bit. The same goes for holiday days and different days of the week, but these correlations are also close to zero, so they're not very significant. Right now, the only clear thing we see is that sales tend to dip when it's raining, but we can't say it's causing the decrease for sure.

Now, we're moving on to the next step: understanding how sales behave over time. The goal here is to get a feel for any patterns or trends that might help us predict future sales. Looking at the chart, we can see a decrease in sales towards the end of 2019, and a big drop during the spring of 2020. This drop in spring is because of a lockdown due to the COVID emergency, with some days showing a peak in demand.


<center><img src="temporal_sales_regular.png" alt="sales-temporal" width="850"></center>


As mentioned earlier, at the end of 2019, there was a decline in sales, followed by a period of stability for the first two months of 2020. Then, sales dropped again during the COVID lockdown. In the seasonal analysis, there's a decrease in sales each month, but this might be influenced by the sharp decline in November 2019. We need to explore further to understand why that happened. At this point, we can't definitively say if there's a consistent trend in sales.


<center><img src="temporal_analysis_regular.png" alt="temporal-analysis" width="950"></center>


As depicted in the following chart, the price experienced a decline during the spring of 2020. However, despite subsequent price increases, sales also rose. This suggests a positive elasticity, indicating that sales tend to increase with price hikes. Notably, this behavior was observed post-lockdown. The chart provides valuable insights into the relationship between sales and pricing dynamics.


<center><img src="price_volume.png" alt="price-volume" width="950"></center>


The following charts illustrate sales patterns across specific days and throughout a typical day. It's evident that the majority of sales occur during typical working hours, which is unsurprising. Client traffic peaks between 6 am and 9 pm, possibly extending to 10 pm, with the most significant activity observed between 8 am to 10 am and 5 pm to 6 pm.


<center><img src="sales_hour.png" alt="sales-hour" width="950"></center>


In terms of the day of the week, the data suggests that the majority of clients purchase gasoline at the beginning and end of the week. This indicates that price increases could be implemented during these periods, considering the surge in sales. However, a deeper analysis is necessary to determine if there's a causal relationship driving these sales patterns.


<center><img src="sales_weekday.png" alt="sales-weekday" width="950"></center>


The following chart provide insights into the impact of rainy days on sales. It's noticeable that on days with minimal rainfall, there is an uptick in the average sales. Now, the task at hand is to ascertain whether rainfall directly influences an increase or decrease in sales.


<center><img src="sales_rainingday.png" alt="sales-rainingday" width="950"></center>


Despite having only a small sample size to gauge the impact on sales, at a surface level, we cannot determine whether sales are increasing or decreasing.


<center><img src="sales_holiday.png" alt="sales-holiday" width="950"></center>


`Insights`<br><br>
From the data depicted in the above charts, several insights emerge. Firstly, there's a notable preference for heightened sales at the beginning and end of the week. This trend could be linked to customers refilling their vehicles for regular commuting at the week's outset and preparing for weekend outings towards its conclusion. Additionally, sales patterns exhibit sensitivity to rainy days, with fewer rainy days correlating with increased sales averages.

Moreover, while the dataset is limited, it suggests that holidays influence sales, with Mexican Revolution Day notably showing higher averages. This uptick could be attributed to heightened travel activity during holiday periods, prompting more individuals to refuel.

Building upon these observations, a pricing strategy could be devised. Adjusting prices slightly upward at the week's start and end, aligning with demand fluctuations, could be beneficial. Similarly, during months with fewer rainy days, implementing price adjustments could be considered. However, it's essential to acknowledge that these are preliminary assumptions, necessitating further causal analysis for validation.

<br>

`Simulating scenearios`

Before delving into that, let's consider the potential scenarios through Monte Carlo simulations, this method offers versatile applications, including:

- *Uncertainty Management:* Sales forecasts inherently carry uncertainty due to various factors like market conditions and customer behavior. Monte Carlo simulation helps model this uncertainty by generating multiple scenarios, offering insights into the range of possible outcomes.

- *Risk Analysis:* By simulating sales under different scenarios, you can assess associated risks. This aids in identifying and preparing for potential challenges that may affect sales performance adversely.

- *Decision Making:* Monte Carlo simulation provides insights into the likelihood of achieving sales targets, enabling informed decision-making. This includes setting realistic targets, resource allocation, and determining pricing strategies based on simulation results.

- *Scenario Planning:* Through Monte Carlo simulation, you can explore different scenarios by adjusting input parameters. This aids in evaluating the impact of various strategies or actions on sales performance, facilitating robust and adaptive planning.

- *Optimization:* Monte Carlo simulation, when combined with optimization techniques, helps identify optimal strategies or decision variables to maximize sales performance. By iteratively simulating scenarios and adjusting variables, solutions that balance risk and reward can be found effectively.

In our case, we aim to explore potential scenarios for the upcoming seven days.


<center><img src="montecarlo.png" alt="montecarlo" width="950"></center>


From the chart above, we observe 10,000 simulated scenarios representing sales for the next 7 days. It's notable that the majority of these scenarios predict sales volumes above 5,000 liters and near to 10,000.


### Price elasticity


Understanding elasticity holds immense importance in economics as it offers insights into how responsive people are to changes in prices or other variables. Elasticity can be envisioned as a gauge of the extent of reaction to change. In this context, we're specifically referring to how demand for a product or service fluctuates in response to alterations in its price.

High elasticity implies that people significantly adjust their purchasing behavior in response to price fluctuations. Conversely, low elasticity suggests minimal changes in buying habits, even when prices vary. This concept is pivotal for both businesses and policymakers. For businesses, awareness of their product's elasticity aids in setting prices strategically. If demand is elastic, caution is warranted in price hikes to avoid substantial sales declines. Conversely, if demand is inelastic, pricing strategies can be more flexible.

In essence, elasticity serves as a measure of consumers' sensitivity to price alterations, thereby assisting businesses and policymakers in making informed decisions.

Analyzing the data from the charts we've seen earlier, it seems that there might be a relationship between price changes and demand fluctuations.

Looking ahead, our main goal is to understand this relationship, especially considering the extraordinary circumstances such as the ongoing pandemic. By taking into account the timing of the pandemic and its effects on consumer behavior, we hope to uncover how demand elasticity has been influenced.

`price vs sales`

Exploring the dynamics of product elasticity amidst the backdrop of a pandemic-induced lockdown reveals intriguing insights. Observing the chart below, it becomes evident that the product exhibits characteristics of inelasticity. Despite a higher price point, sales remain robust, indicating a lesser degree of responsiveness to price changes. However, it's crucial to note that this trend is intricately tied to the unique circumstances of the lockdown imposed due to the pandemic. Let's delve deeper into the implications of this phenomenon.


<center><img src="log_sales_vs_log_price.png" alt="price_vs_sales" width="950"></center>


In the charts above, we can discern the connection between price and sales, as well as these variables when logged.


`OLS model`


The next step involves determining the sensitivity of sales to price changes, taking into account the following relation:

$$
Y = \beta_0 + \beta_1X_i
$$

where $\beta_0$ is the intercept and $\beta_1$ represents the price sensitivity, it's important to note that the relationship isn't a straightforward percentage proportion and doesn't directly represent elasticity. *Elasticity,* in essence, measures the percentage change in sales relative to the percentage change in price. To achieve that, we must take into account the following relationship:

$$
ln(Y) = ln(\beta_0) + ln(\beta_1*X_i)
$$

Ultimately, we'll arrive at the following equation.

$$
ln(Y) = \beta_0 + \beta_1ln(X_i)
$$

Now, with the logarithmic relationship between sales and prices, we can derive the elasticity, represented by $\beta_1$.


<center><img src="OLS_result.png" alt="OLS-result" width="400"></center>


Following the OLS regression, we find a coefficient of *3.49* for $\beta_1$, indicating an elasticity of *3.49.* This suggests that sales tend to rise alongside price increases. However, this assumption may not hold true in a typical market where elasticity is negative. The observed positive effect could be attributed to the transition out of lockdown and the resumption of economic activity. During this period, both prices and sales may have increased. Nonetheless, it's crucial to acknowledge that the impact of price on sales could be minimal.

To gain a better understanding of elasticity behavior, we attempt to forecast the volume using the following equation:

$$ Y = \alpha \cdot P^b $$
where
$$\alpha=e^a$$
and, where *a* represents the intercept of the Ordinary Least Squares (OLS) model and *b* signifies the elasticity.

*Note: Keep in mind that for the present model, we are solely taking the price into consideration as a variable.*


<center><img src="predicted_price.png" alt="price-predicted" width="950"></center>


As depicted in the chart above, our model's predictive accuracy regarding volume is not particularly high. However, it does provide insight into volume trends, particularly when considering price fluctuations.

It's important to acknowledge that our output is influenced by various factors such as time of day, day of the week, and weather conditions, not solely reliant on price.


`optimal price`


One crucial aspect of running a business is determining the ideal selling price. With the current sales model:

$$
demand=\alpha price^b
$$

our aim is to estimate the optimal price.However, before proceeding, we must also analyze the price dynamics and incorporate the final costs into our considerations.


<center><img src="boxplot_price_cost.png" alt="boxplot-price-cost" width="950"></center>


As illustrated in the box plot, our median price is slightly above \\$19, with a few outliers below \\$14. However, these outliers are uncommon and likely result from the notable cost reductions during the COVID-19 pandemic. With our positive elasticity, we lean towards setting price limits between \\$17.99 and \\$23.99. This range strikes a balance, allowing us to sustain profitability while responding to pandemic-driven shifts in market dynamics.

For the next step we try with Bayesian optimization to refine our pricing strategy. This method aims to approximate the optimal solution by utilizing probabilistic functions. By leveraging Bayesian optimization, we strive to navigate the intricate realm of pricing decisions efficiently. Our approach relies on probabilistic reasoning to help us maximize our desired outcomes effectively.


<center><img src="optimal_price.png" alt="optimal-price" width="950"></center>


As observed in the graph, our analysis points to an optimal price of $23.99, which aligns closely with our elasticity coefficient of 3.49. This coefficient indicates a positive correlation between price and sales, implying that higher prices correspond to increased sales. However, it's important to acknowledge that this may not fully capture the complexity of the market dynamics. While recent data show a rise in sales despite price increases, historical sales patterns suggest that initial price adjustments had minimal impact on sales. This suggests a market that may be less responsive to price changes, hinting at a degree of inelasticity.

Moreover, our current demand model focuses solely on price, overlooking potential factors that could also influence sales. Incorporating additional variables could lead to a more comprehensive and accurate model. Nevertheless, our current findings suggest that our market may not be as price-sensitive as initially assumed.


<center><img src="1st_stage.png" alt="1st-stage" width="250"></center>

```python

```
