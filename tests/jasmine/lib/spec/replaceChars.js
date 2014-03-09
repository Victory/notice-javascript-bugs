describe("Replace Chars", function () {

  it("No flags No problem", function () {
    var needle = 'a';
    var haystack = 'a';
    var replace = 'b';
    var expected = 'b';

    var actual = njbValidation.replaceChars(needle, replace, haystack);
    expect(expected).toEqual(actual);
  });

  it("Replaces a single 'a' with a single 'b'", function () {
    var needle = 'a';
    var haystack = 'a';
    var replace = 'b';
    var expected = 'b';

    var actual = njbValidation.replaceChars(needle, replace, haystack);
    expect(expected).toEqual(actual);
  });


  it("Replaces a single 'a' with a single 'b' in 'aaa'", function () {
    var needle = 'a';
    var haystack = 'aaa';
    var replace = 'b';
    var expected = 'baa';

    var actual = njbValidation.replaceChars(needle, replace, haystack);
    expect(expected).toEqual(actual);
  });

  it("Replaces all 'a' with 'b' in 'aaa'", function () {
    var needle = 'a';
    var haystack = 'aaa';
    var replace = 'b';
    var flags = 'g';
    var expected = 'bbb';
    var actual = njbValidation.replaceChars(needle, replace, haystack, flags);
    expect(expected).toEqual(actual);
  });

});