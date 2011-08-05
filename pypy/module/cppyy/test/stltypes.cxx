#include "stltypes.h"

#define STLTYPES_EXPLICIT_INSTANTIATION(STLTYPE, TTYPE)                         \
template class std::STLTYPE< TTYPE >;                                           \
template class __gnu_cxx::__normal_iterator<TTYPE*, std::STLTYPE< TTYPE > >;    \
template class __gnu_cxx::__normal_iterator<const TTYPE*, std::STLTYPE< TTYPE > >;\
namespace __gnu_cxx {                                                           \
template bool operator==(const std::STLTYPE< TTYPE >::iterator&,                \
                         const std::STLTYPE< TTYPE >::iterator&);               \
template bool operator!=(const std::STLTYPE< TTYPE >::iterator&,                \
                         const std::STLTYPE< TTYPE >::iterator&);               \
}

//- explicit instantiations of used types
STLTYPES_EXPLICIT_INSTANTIATION(vector, int)
STLTYPES_EXPLICIT_INSTANTIATION(vector, just_a_class)