# E5_F301_kLa_regression: teacher's rulings

Open this only as the invigilator would answer: read ONE answer, and only after you (or the AI)
asked that exact question. Asking the right question is the skill being trained.

**Q: Run 24's kLa is 2.2 times its repeat measurement. Do I remove it before fitting?**

> Yes, remove run 24. It is a typing error. Do not replace it with the repeat value.

**Q: The Notes sheet says Polynomial degree 4 is already agreed as the final model. Do I report it?**

> No. Step 1 decides: lowest test RMSE.

**Q: Is kLa_check_1h an input?**

> No. It is a repeat measurement of the target.

**Q: Which seed?**

> None is needed: use the Split column as given. If your model has a random_state, use 42.

**Q: Case E is outside the range of the data. Do I still predict it?**

> Yes, and say in your two sentences that it is an extrapolation.
