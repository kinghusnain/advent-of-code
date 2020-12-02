import org.junit.jupiter.api.Test

class Day02Tests {
    @Test
    fun parser() {
        val rec = "1-3 a: abcde".toPasswordRecord1()
        assert(rec.policyMin == 1)
        assert(rec.policyMax == 3)
        assert(rec.policyChar == 'a')
        assert(rec.password == "abcde")
    }

    @Test
    fun charCount() {
        val rec = PasswordRecord1(1, 3, 'a', "abcdefa")
        assert(rec.policyCharCount() == 2)
    }

    @Test
    fun isValid() {
        assert(PasswordRecord1(1, 3, 'a', "abba").isValid())
        assert(!PasswordRecord1(1, 2, 'b', "babba").isValid())
    }

    @Test
    fun validRecordCount() {
        val recs = listOf(
            PasswordRecord1(1,3,'a', "abcde"),
            PasswordRecord1(1,3, 'b', "cdefg"),
            PasswordRecord1(2,9,'c', "ccccccccc")
        )
        assert(recs.validRecords() == 2)
    }
}